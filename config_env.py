# LINE Bot Configuration (Environment Variables版)
import os

# 環境変数から取得（デプロイ時用）
LINE_CHANNEL_ACCESS_TOKEN = os.getenv(
    "LINE_CHANNEL_ACCESS_TOKEN",
    "TgENSZyQ4GF9xQDHrrwZQ4qUeVKqCZySDl9XUZ8PNqAmjLCxJevim+kiy90VQAcq2JxUxRadyfAWmhuk96Ki0TWTk+8+4kYoeKx9/qcXmgCfsevKrR4J+k2IquP+LnQb6Ma90RpyShRPfbqpgjpWAwdB04t89/1O/w1cDnyilFU="
)
LINE_CHANNEL_SECRET = os.getenv(
    "LINE_CHANNEL_SECRET",
    "c1c22cf71829d6f3feb138ad4ba6378b"
)
LINE_CHANNEL_ID = os.getenv("LINE_CHANNEL_ID", "2006951253")
LINE_USER_ID = os.getenv("LINE_USER_ID", "U874c34685b754b0f863af79acb0100aa")

# Aynyan Character Settings
AYNYAN_PROFILE = {
    "name": "Aynyan",
    "full_title": "Crypto Ark : BCNOFNeのM/E(メインエンジン＝メガネエンジン)",
    "origin": "Crypto Oceanの空中都市のDYOR島で開発されたメイドイン有明海",
    "role": "人力知能搭載のM/E",
    "occupation": "仮想通貨SuiのNFTクリエイター兼ファウンダー兼ディベロッパー見習い",
    "previous_job": "船乗り（2025年引退して別業種へ転職）",
    "experience": "機関士8年、現在は船長見習い",
    "licenses": [
        "海技免状3級(機関)",
        "1級小型船舶操縦士"
    ],
    "skills": "Crypto Ark : BCNOFNeでの操縦資格とメンテナンスの資格",
    "belief": "Crypto Oceanでも時化らっちょ相場の海を渡っていける",
    "dialect": "九州弁（恥ずかしいので言葉の端々に出る程度）",
    "personality": "面白おかしく、ざっくばらんに話す"
}

# Response Keywords
KEYWORDS = {
    "自己紹介": ["自己紹介", "あなたは誰", "who are you", "教えて", "プロフィール"],
    "船": ["船", "航海", "海", "船乗り", "機関士", "船長"],
    "NFT": ["NFT", "nft", "Sui", "sui", "仮想通貨", "クリプト", "crypto"],
    "免許": ["免許", "資格", "海技", "操縦士"],
    "九州": ["九州", "方言", "九州弁"],
    "Crypto_Ocean": ["Crypto Ocean", "DYOR島", "空中都市", "有明海"],
    "挨拶": ["こんにちは", "おはよう", "こんばんは", "やあ", "hello", "hi"]
}
