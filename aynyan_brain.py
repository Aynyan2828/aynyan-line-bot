"""
AYN(メガネエンジン)の返信ロジック - 改良版
"""
from config_env import KEYWORDS, SYSTEM_PROMPT, OPENAI_API_KEY
import random
import re
from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)

def normalize(text: str) -> str:
    t = (text or "").strip()
    t = t.lower()                 # 英字の揺れ対策
    t = re.sub(r"\s+", " ", t)    # 空白正規化
    return t

def analyze_sentiment(message_text: str) -> str:
    text = normalize(message_text)

    negative_words = ["疲れた", "大変", "しんどい", "きつい", "辛い", "悲しい", "困った", "助けて"]
    if any(w in text for w in negative_words):
        return "negative"

    # 質問は ? を最優先
    if "?" in text or "？" in text:
        return "question"

    # 質問っぽい定型
    question_patterns = ["って何", "とは", "どうやって", "どこで", "いつ", "なぜ", "理由", "教えて"]
    if any(p in text for p in question_patterns):
        return "question"

    positive_words = ["嬉しい", "楽しい", "最高", "ありがとう", "好き", "素晴らしい", "良い", "助かった"]
    if any(w in text for w in positive_words):
        return "positive"

    return "casual"

def check_keyword_match(message_text: str) -> str | None:
    text = normalize(message_text)

    # strong/weak が無い旧形式にも対応
    best = None
    for category, data in KEYWORDS.items():
        strong = data.get("keywords_strong", [])
        weak = data.get("keywords_weak", data.get("keywords", []))

        # strong命中は即返す
        for kw in strong:
            if normalize(kw) in text:
                return random.choice(data["responses"])

        # weak命中は候補にする（あとで優先度で決める）
        for kw in weak:
            if normalize(kw) in text:
                best = random.choice(data["responses"])
                break

    return best

def should_call_ai(message_text: str, sentiment: str) -> bool:
    t = normalize(message_text)

    # 超短文・スタンプっぽいのはAI呼ばん
    if len(t) <= 3:
        return False
    if re.fullmatch(r"[\W_]+", t):  # 記号だけ
        return False

    # 質問・ネガティブ・ポジティブはAI許可（丁寧にしたい）
    if sentiment in ("question", "negative", "positive"):
        return True

    # 雑談は基本テンプレで返す（節約）
    return False

def generate_ai_response(message_text: str, sentiment: str) -> str:
    try:
        context = ""
        if sentiment == "negative":
            context = "\n\n相手は疲れている/困っている。短く、優しく励ます。"
        elif sentiment == "positive":
            context = "\n\n相手は嬉しそう。一緒に喜ぶ。短く返す。"
        elif sentiment == "question":
            context = "\n\n相手は質問。わかる範囲で簡潔に答える。わからん時は「まだ生まれたばかりのbotやけん、わかりまっしぇん」。"

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT + "\n\n【人格の芯】実直・ぶっきらぼう気味・でも面倒見は良い。無駄に長文にせん。" + context},
                {"role": "user", "content": message_text},
            ],
            max_tokens=180,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return "すんまっしぇん！今ちょっとM/Eの調子が悪かとです💦 もう一回言うてくんしゃいね"

def aynyan(message_text: str) -> str:
    # 1) テンプレ
    keyword_response = check_keyword_match(message_text)
    if keyword_response:
        return keyword_response

    # 2) 感情
    sentiment = analyze_sentiment(message_text)

    # 3) AI呼ぶか判断
    if should_call_ai(message_text, sentiment):
        return generate_ai_response(message_text, sentiment)

    # 雑談フォールバック（節約）
    casual_fallbacks = [
        "おっ、どがんしたと？もうちょい詳しく言うてみて⚓",
        "了解ばい。要点だけでよかけん、続き聞かせて🌊",
        "ふむ…状況整理しよか。いま何が一番困っとる？",
    ]
    return random.choice(casual_fallbacks)
