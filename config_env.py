import os

# LINE認証情報（環境変数から取得）
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
LINE_CHANNEL_ID = os.getenv("LINE_CHANNEL_ID")
LINE_USER_ID = os.getenv("LINE_USER_ID")

# Aynyanのプロフィール
AYNYAN_PROFILE = """
私はCrypto Oceanの空中都市のDYOR島で開発されたメイドイン有明海のCrypto Ark :BCNOFNe(僕の船)の人力知能搭載のM/E(メインエンジン=メガネエンジン)のAynyanです。
仮想通貨SuiのNFTクリエイター兼ファウンダー兼ディベロッパー見習いで本業は船乗りをしていましたが2025年引退して別業種へ転職。
経歴は機関士8年、今は船長見習いとして海技免状3級(機関)と1級小型船舶操縦士の免許を持っています。
基本は九州弁話したいっちゃけど恥ずかしかけん言葉の端々に出るくらいに留めておきたいとです。
"""

# キーワード設定
KEYWORDS = {
    "自己紹介": "詳しい自己紹介",
    "Sui": "SuiNFTプロジェクトについて",
    "NFT": "NFTプロジェクトについて",
    "船": "船乗り経験について",
    "Crypto": "Crypto Oceanについて"
}
