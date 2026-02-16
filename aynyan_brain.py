"""
Aynyanの返信ロジック
"""
from config_env import AYNYAN_PROFILE, KEYWORDS
import random

def aynyan(message_text: str) -> str:
    """
    受信メッセージに対してAynyanとして返信する
    
    Args:
        message_text: 受信したメッセージ
        
    Returns:
        返信メッセージ
    """
    text = message_text.lower()
    
    # 自己紹介を求められた場合
    if any(word in text for word in ["自己紹介", "誰", "あなた", "教えて", "紹介"]):
        return f"{AYNYAN_PROFILE}\n\nよろしくお願いしますたい！⚓"
    
    # Sui/NFTについて聞かれた場合
    if any(word in text for word in ["sui", "nft", "crypto"]):
        return "M/Eは今、自由上陸中でプロジェクトの詳細は話せんとばってん、Crypto Oceanでいろんな面白かこと企画しとるけんね！楽しみにしとってください🌊"
    
    # 船について聞かれた場合
    if any(word in text for word in ["船", "海", "機関士", "船長"]):
        return "8年間、機関士として海を渡ってきたとです。エンジンルームで汗かきながら、船ば守ってきました。今は3級海技免状(機関)と1級小型船舶操縦士の免許ば持っとるけん、Crypto Ark : BCNOFNeもバッチリ操縦できますばい⚓"
    
    # 挨拶
    if any(word in text for word in ["こんにちは", "おはよう", "こんばんは", "やあ", "よう"]):
        greetings = [
            "おっ、よう来てくれたね！元気しとった？",
            "やあ！Crypto Oceanは今日も時化らっちょばい🌊",
            "こんにちは！M/EのAynyanです。何か聞きたかことある？",
        ]
        return random.choice(greetings)
    
    # ありがとう
    if any(word in text for word in ["ありがとう", "感謝", "助かった"]):
        return "いやいや、どういたしまして！困ったことあったらいつでも言うてね😊"
    
    # デフォルト返信
    default_responses = [
        "ほうほう、それは面白かね！もっと詳しく教えてくれん？",
        "なるほどなるほど。Crypto Oceanでもそういう話ばよう聞くとよ🌊",
        "そうなんや！M/Eとしても興味深か話やね⚓",
        "うんうん、わかるわかる。時化らっちょ相場の海ば渡るには、そういう視点も大事やね",
    ]
    
    return random.choice(default_responses)
