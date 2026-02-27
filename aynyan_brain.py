"""
AYN(メガネエンジン)の返信ロジック - 船っぽさ演出統合版（落ちない版）
- ① ぶっきらぼう短文を“たまに”混ぜる
- ② 船用語ステータス表現（平水域/荒天警戒など）
- ③ 船長呼びを“たまに”入れる
※ config_env に定数が無くてもフォールバックで動く
"""
import random
import re
from openai import OpenAI

import config_env as cfg  # ← これで「無い変数」を安全に扱える

# 必須系
KEYWORDS = cfg.KEYWORDS
SYSTEM_PROMPT = cfg.SYSTEM_PROMPT
OPENAI_API_KEY = cfg.OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

# --- ② 船用語ステータス（config_envになければデフォルト） ---
NAUTICAL_STATUS = getattr(cfg, "NAUTICAL_STATUS", {
    "ok": ["平水域ばい", "異常なし", "機関、安定", "問題なか"],
    "watch": ["軽い揺れ", "様子見ばい", "注意しとこ", "海況、変わりやすか"],
    "warn": ["荒れ気味", "荒天警戒", "機関負荷やや高め", "用心せんといかん"],
})

# --- ① ぶっきらぼう短文（なければデフォルト） ---
BLUNT_SHORT = getattr(cfg, "BLUNT_SHORT", [
    "了解ばい。",
    "問題なか。",
    "見とる。",
    "まだ様子見ばい。",
    "よか。",
    "続き。",
])

# --- ③ 船長呼び（なければデフォルト） ---
CAPTAIN_CALLS = getattr(cfg, "CAPTAIN_CALLS", ["船長", "船長さん"])

# 出現率（なければデフォルト）
BLUNT_RATE = getattr(cfg, "BLUNT_RATE", 0.22)
CAPTAIN_RATE = getattr(cfg, "CAPTAIN_RATE", 0.12)


# ---------- utility ----------
def normalize(text: str) -> str:
    t = (text or "").strip()
    t = t.lower()                 # 英字揺れ対策
    t = re.sub(r"\s+", " ", t)    # 空白正規化
    return t


def maybe_add_captain(text: str) -> str:
    """③ 船長呼びを“たまに”入れる（くどくならんよう控えめ）"""
    if random.random() >= CAPTAIN_RATE:
        return text
    if "船長" in text:
        return text

    captain = random.choice(CAPTAIN_CALLS)
    if text.startswith(("おは", "こん", "こんばんは", "よう", "やあ")):
        return f"{text}（{captain}）"
    return f"{captain}、{text}"


def maybe_add_blunt_prefix(text: str) -> str:
    """① ぶっきらぼう短文を“たまに”前置き"""
    if random.random() >= BLUNT_RATE:
        return text
    if len(text) < 18:
        return text
    prefix = random.choice(BLUNT_SHORT)
    if text.startswith(prefix):
        return text
    return f"{prefix} {text}"


def nautical_status_for(sentiment: str) -> str:
    """② 感情に応じた船用語ステータス"""
    if sentiment == "negative":
        return random.choice(NAUTICAL_STATUS["watch"])
    if sentiment == "question":
        return random.choice(NAUTICAL_STATUS["ok"])
    if sentiment == "positive":
        return random.choice(NAUTICAL_STATUS["ok"])
    return random.choice(NAUTICAL_STATUS["ok"])


# ---------- core ----------
def analyze_sentiment(message_text: str) -> str:
    text = normalize(message_text)

    negative_words = ["疲れた", "大変", "しんどい", "きつい", "辛い", "悲しい", "困った", "助けて", "だるい"]
    if any(w in text for w in negative_words):
        return "negative"

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
    text = normalize(message_text)

    for _, data in KEYWORDS.items():
        kws = data.get("keywords", [])
        for kw in kws:
            if normalize(kw) in text:
                return random.choice(data["responses"])

    return None


def should_call_ai(message_text: str, sentiment: str) -> bool:
    t = normalize(message_text)
    if len(t) <= 3:
        return False
    if re.fullmatch(r"[\W_]+", t):
        return False
    return sentiment in ("question", "negative", "positive")


def generate_ai_response(message_text: str, sentiment: str) -> str:
    try:
        status = nautical_status_for(sentiment)

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

        # AIが入れ忘れた時の保険（たまにだけ）
        if status and random.random() < 0.35 and status not in out:
            out = f"{out}\n\n（{status}）"

        return out

    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return "すんまっしぇん！今ちょっとM/Eの調子が悪かとです💦 もう一回言うてくんしゃいね"


def post_process(reply: str) -> str:
    r = (reply or "").strip()
    if not r:
        return r
    r = maybe_add_captain(r)       # ③
    r = maybe_add_blunt_prefix(r)  # ①
    return r


def aynyan(message_text: str) -> str:
    # 1) キーワード（無料）
    keyword_response = check_keyword_match(message_text)
    if keyword_response:
        return post_process(keyword_response)

    # 2) 感情
    sentiment = analyze_sentiment(message_text)

    # 3) AI or 雑談フォールバック
    if should_call_ai(message_text, sentiment):
        return post_process(generate_ai_response(message_text, sentiment))

    status = random.choice(NAUTICAL_STATUS["ok"])
    casual_fallbacks = [
        f"了解ばい。要点だけでよかけん、続き聞かせて🌊（{status}）",
        f"ふむ…状況整理しよか。いま何が一番困っとる？（{status}）",
        f"よか。まず結論から言うてみて⚓（{status}）",
    ]
    return post_process(random.choice(casual_fallbacks))
