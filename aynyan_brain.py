"""
AYN(メガネエンジン)の返信ロジック - AI統合強化版
"""
from config_env import KEYWORDS, SYSTEM_PROMPT, OPENAI_API_KEY
import random
import openai

# OpenAI APIの設定
openai.api_key = OPENAI_API_KEY

def analyze_sentiment(message_text: str) -> str:
    """
    メッセージの感情を分析する
    
    Args:
        message_text: 受信したメッセージ
        
    Returns:
        感情タイプ: 'positive', 'negative', 'question', 'casual'
    """
    text = message_text.lower()
    
    # ネガティブな感情
    negative_words = ["疲れた", "大変", "しんどい", "きつい", "辛い", "悲しい", "困った", "助けて"]
    if any(word in text for word in negative_words):
        return 'negative'
    
    # 質問
    if "?" in text or "？" in text or any(word in text for word in ["何", "どう", "いつ", "どこ", "誰", "なぜ", "どれ"]):
        return 'question'
    
    # ポジティブな感情
    positive_words = ["嬉しい", "楽しい", "最高", "ありがとう", "好き", "素晴らしい", "良い"]
    if any(word in text for word in positive_words):
        return 'positive'
    
    # デフォルトは雑談
    return 'casual'


def check_keyword_match(message_text: str) -> str:
    """
    キーワードマッチングで返信を生成
    
    Args:
        message_text: 受信したメッセージ
        
    Returns:
        返信メッセージ（マッチしない場合はNone）
    """
    text = message_text.lower()
    
    # 各カテゴリをチェック
    for category, data in KEYWORDS.items():
        for keyword in data["keywords"]:
            if keyword in text:
                return random.choice(data["responses"])
    
    return None


def generate_ai_response(message_text: str, sentiment: str) -> str:
    """
    OpenAI APIを使用してAI返信を生成
    
    Args:
        message_text: 受信したメッセージ
        sentiment: 感情タイプ
        
    Returns:
        AI生成の返信メッセージ
    """
    try:
        # 感情に応じたコンテキストを追加
        context = ""
        if sentiment == 'negative':
            context = "\n\n相手は疲れているか困っているようです。優しく励ましてください。"
        elif sentiment == 'positive':
            context = "\n\n相手は嬉しそうです。一緒に喜んでください。"
        elif sentiment == 'question':
            context = "\n\n相手は質問をしています。わかる範囲で答えてください。わからない場合は素直に「まだ生まれたばかりのbotやけん、わかりまっしぇん」と答えてください。"
        
        # OpenAI APIを呼び出し
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT + context},
                {"role": "user", "content": message_text}
            ],
            max_tokens=150,
            temperature=0.8,
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        # エラー時のフォールバック
        print(f"OpenAI API Error: {e}")
        return "すんまっしぇん！今ちょっとM/Eの調子が悪かとです💦 もう一回言うてくんしゃいね"


def aynyan(message_text: str) -> str:
    """
    受信メッセージに対してAYNとして返信する
    
    フロー:
    1. キーワードマッチング（高速・無料）
    2. 感情分析
    3. AI返信生成（有料）
    
    Args:
        message_text: 受信したメッセージ
        
    Returns:
        返信メッセージ
    """
    # Step 1: キーワードマッチング
    keyword_response = check_keyword_match(message_text)
    if keyword_response:
        return keyword_response
    
    # Step 2: 感情分析
    sentiment = analyze_sentiment(message_text)
    
    # Step 3: AI返信生成
    ai_response = generate_ai_response(message_text, sentiment)
    
    return ai_response
