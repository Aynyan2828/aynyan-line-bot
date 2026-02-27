"""
AYN(メガネエンジン)の返信ロジック - 船っぽさ演出統合版（①②③）
- ① ぶっきらぼう短文を“たまに”混ぜる
- ② 船用語ステータス表現（平水域/荒天警戒など）
- ③ 船長呼びを“たまに”入れる
"""
from config_env import (
    KEYWORDS,
    SYSTEM_PROMPT,
    OPENAI_API_KEY,
    NAUTICAL_STATUS,
    BLUNT_SHORT,
    CAPTAIN_CALLS,
    BLUNT_RATE,
    CAPTAIN_RATE,
)

import random
import re
from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)


# ---------- utility ----------
def normalize(text: str) -> str:
    t = (text or "").strip()
    t = t.lower()                 # 英字揺れ対策
    t = re.sub(r"\s+", " ", t)    # 空白正規化
    return t


def maybe_add_captain(text: str) -> str:
    """③ 船長呼びを“たまに”頭につける（くどくならんように控えめ）"""
    if random.random() >= CAPTAIN_RATE:
        return text

    # すでに呼んどる/不自然な時はスキップ
    if "船長" in text:
        return text

    captain = random.choice(CAPTAIN_CALLS)
    # 先頭が挨拶っぽい時は後ろに、そうでなければ頭に
    if text.startswith(("おは", "こん", "こんばんは", "よう", "やあ")):
        return f"{text}（{captain}）"
    return f"{captain}、{text}"


def maybe_add_blunt_prefix(text: str, force: bool = False) -> str:
    """① ぶっきらぼう短文を“たまに”前置きとして混ぜる"""
    if not force and random.random() >= BLUNT_RATE:
        return text

    # 長文にだけ添える（短文に短文はクドい）
    if len(text) < 18 and not force:
        return text

    prefix = random.choice(BLUNT_SHORT)
    # すでに同じ語感の時はやめる
    if text.startswith(prefix):
        return text
    return f"{prefix} {text}"


def nautical_status_for(sentiment: str) -> str:
    """② 感情に応じた船用語ステータスを選ぶ"""
    if sentiment == "negative":
        return random.choice(NAUTICAL_STATUS["watch"])
    if sentiment == "question":
        return random.choice(NAUTICAL_STATUS["ok"])
    if sentiment == "positive":
        return random.choice(NAUTICAL_STATUS["ok"])
    return random.choice(NAUTICAL_STATUS["ok"])


# ---------- core ----------
def analyze_sentiment(message_text: str) -> str:
    """
    メッセージの感情を分析
    Returns: 'positive', 'negative', 'question', 'casual'
    """
    text = normalize(message_text)

    negative_words = ["疲れた", "大変", "しんどい", "きつい", "辛い", "悲しい", "困った", "助けて", "だるい"]
    if any(w in text for w in negative_words):
        return "negative"

    # 質問判定：?優先＋定型
    if "?" in text or "？" in text:
        return "question"
    question_patterns = ["って何", "とは", "どうやって", "どこで", "いつ", "なぜ", "理由", "教えて", "方法"]
    if any(p in text for p in question_patterns):
        return "question"

    positive_words = ["嬉しい", "楽しい", "最高", "ありがとう", "好き", "素晴らしい", "良い", "助かった", "神"]
    if any(w in text for w in positive_words):
        return "positive"

    return "casual"


def check_keyword_match(message_text: str) -> str | None:
    """
    キーワードマッチングで返信を生成（無料）
    """
    text = normalize(message_text)

    for _, data in KEYWORDS.items():
        # 旧形式 keywords 互換
        kws = data.get("keywords", [])
        for kw in kws:
            if normalize(kw) in text:
                return random.choice(data["responses"])

    return None


def generate_ai_response(message_text: str, sentiment: str) -> str:
    """
    OpenAI APIで返信生成（有料）
    """
    try:
        # ② 船用語ステータスを“ひとこと”混ぜる
        status = nautical_status_for(sentiment)

        # 感情に応じた指示（短く）
        context = ""
        if sentiment == "negative":
            context = "\n\n相手は疲れている/困っている。短く、優しく励ます。説教しない。"
        elif sentiment == "positive":
            context = "\n\n相手は嬉しそう。短く一緒に喜ぶ。"
        elif sentiment == "question":
            context = "\n\n相手は質問。簡潔に答える。わからん時は「まだ生まれたばかりのbotやけん、わかりまっしぇん」。"

        system = (
            SYSTEM_PROMPT
            + "\n\n【人格の芯】実直・ぶっきらぼう気味・でも面倒見は良い。無駄に長文にせん。"
            + "\n【船っぽさ】たまに船用語の状態表現（平水域/様子見/荒天警戒）を一言混ぜる。"
            + context
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": message_text},
            ],
            max_tokens=180,
            temperature=0.7,
        )

        out = response.choices[0].message.content.strip()

        # ② 状態ひとことを末尾に“たまに”添える（AIが入れ忘れたとき用）
        if status and random.random() < 0.35 and status not in out:
            out = f"{out}\n\n（{status}）"

        return out

    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return "すんまっしぇん！今ちょっとM/Eの調子が悪かとです💦 もう一回言うてくんしゃいね"


def should_call_ai(message_text: str, sentiment: str) -> bool:
    """
    節約：AI呼ぶべきか
    """
    t = normalize(message_text)

    # 超短文・記号だけは呼ばん
    if len(t) <= 3:
        return False
    if re.fullmatch(r"[\W_]+", t):
        return False

    # 質問/ネガ/ポジはAIで丁寧に
    if sentiment in ("question", "negative", "positive"):
        return True

    # 雑談は基本テンプレで返す（節約）
    return False


def post_process(reply: str) -> str:
    """
    ①③の演出を最終段で適用（くどさ防止のため最後にまとめて）
    """
    r = (reply or "").strip()
    if not r:
        return r

    # ③ 船長呼びを“たまに”
    r = maybe_add_captain(r)

    # ① ぶっきらぼう短文を“たまに”前置き
    r = maybe_add_blunt_prefix(r)

    return r


def aynyan(message_text: str) -> str:
    """
    受信メッセージに対してAYNとして返信する
    1) キーワード（無料）
    2) 感情分析
    3) AI（有料） or 雑談フォールバック（節約）
    """
    # 1) キーワード
    keyword_response = check_keyword_match(message_text)
    if keyword_response:
        return post_process(keyword_response)

    # 2) 感情
    sentiment = analyze_sentiment(message_text)

    # 3) AI or fallback
    if should_call_ai(message_text, sentiment):
        return post_process(generate_ai_response(message_text, sentiment))

    # 雑談フォールバック（船っぽさ②を軽く）
    status = random.choice(NAUTICAL_STATUS["ok"])
    casual_fallbacks = [
        f"了解ばい。要点だけでよかけん、続き聞かせて🌊（{status}）",
        f"ふむ…状況整理しよか。いま何が一番困っとる？（{status}）",
        f"よか。まず結論から言うてみて⚓（{status}）",
    ]
    return post_process(random.choice(casual_fallbacks))
