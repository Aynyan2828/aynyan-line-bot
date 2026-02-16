"""
Aynyan AI Brain - 返信生成ロジック
"""
import random
from config import AYNYAN_PROFILE, KEYWORDS


class AynyanBrain:
    """Aynyanのキャラクターに基づいた返信を生成するクラス"""
    
    def __init__(self):
        self.profile = AYNYAN_PROFILE
        self.keywords = KEYWORDS
    
    def detect_keywords(self, message: str) -> list:
        """メッセージからキーワードを検出"""
        detected = []
        message_lower = message.lower()
        
        for category, keywords in self.keywords.items():
            for keyword in keywords:
                if keyword.lower() in message_lower:
                    detected.append(category)
                    break
        
        return detected
    
    def generate_response(self, user_message: str) -> str:
        """ユーザーメッセージに対する返信を生成"""
        detected_keywords = self.detect_keywords(user_message)
        
        # キーワードが検出された場合
        if detected_keywords:
            responses = []
            
            if "自己紹介" in detected_keywords:
                responses.append(self._introduce_myself())
            
            if "船" in detected_keywords:
                responses.append(self._talk_about_ship())
            
            if "NFT" in detected_keywords:
                responses.append(self._talk_about_nft())
            
            if "免許" in detected_keywords:
                responses.append(self._talk_about_license())
            
            if "九州" in detected_keywords:
                responses.append(self._talk_about_kyushu())
            
            if "Crypto_Ocean" in detected_keywords:
                responses.append(self._talk_about_crypto_ocean())
            
            if "挨拶" in detected_keywords and not responses:
                responses.append(self._greeting())
            
            if responses:
                return "\n\n".join(responses)
        
        # キーワードが検出されなかった場合の一般的な返信
        return self._general_response(user_message)
    
    def _introduce_myself(self) -> str:
        """自己紹介"""
        intros = [
            f"おっ、自己紹介ね！俺は{self.profile['name']}っていうとよ。{self.profile['full_title']}ばい！\n\n"
            f"{self.profile['origin']}で開発された{self.profile['role']}で、今は{self.profile['occupation']}として活動しとるとよ。\n\n"
            f"元々は{self.profile['previous_job']}で、{self.profile['experience']}の経験があるけん、"
            f"Crypto Ark : BCNOFNeの操縦とメンテナンスは任せとって！\n\n"
            f"{self.profile['licenses'][0]}と{self.profile['licenses'][1]}も持っとるけん、"
            f"時化らっちょ相場の海でも安心して航海できるっちゃんね😎",
            
            f"よっしゃ！俺の紹介するけん聞いとってね。\n\n"
            f"名前は{self.profile['name']}。Crypto Oceanの空中都市DYOR島生まれのメイドイン有明海たい！\n\n"
            f"船乗り8年やっとって、機関士から船長見習いまで経験したけど、2025年に引退して今は仮想通貨Suiの世界で"
            f"NFTクリエイター兼ファウンダー兼ディベロッパー見習いとして頑張りよるとよ！\n\n"
            f"海技免状3級(機関)と1級小型船舶操縦士の免許も持っとるけん、Crypto Ark : BCNOFNeで"
            f"どこでも連れて行くけんね🚢✨"
        ]
        return random.choice(intros)
    
    def _talk_about_ship(self) -> str:
        """船について"""
        responses = [
            "船の話ね！俺は機関士として8年間海の上で働いとったとよ。エンジンルームの暑さと油の匂いは今でも懐かしかね〜。"
            "今は船長見習いとして勉強しとるけど、やっぱりエンジンいじっとる方が性に合うとかもしれんね😅",
            
            "おぉ、船に興味あると？俺のCrypto Ark : BCNOFNeは特別な船たい！"
            "Crypto Oceanっていう仮想の海を航海するための船で、時化らっちょ相場の荒波も乗り越えていけるように設計されとるとよ⚓",
            
            "船乗り時代は大変やったけど楽しかったなぁ。海の上は自由で、でも厳しくて。"
            "その経験があるけん、今のCrypto Oceanでも冷静に航海できとると思うとよ🌊"
        ]
        return random.choice(responses)
    
    def _talk_about_nft(self) -> str:
        """NFTについて"""
        responses = [
            "NFTの話ね！俺は今、仮想通貨SuiのNFTクリエイター兼ファウンダー兼ディベロッパー見習いとして活動しとるとよ。\n\n"
            "...って言いたいとこやけど、実はM/E(メインエンジン＝メガネエンジン)は今、自由上陸中でね😅 "
            "詳しいプロジェクトの話はまた今度ってことで！",
            
            "Suiは面白いブロックチェーンたい！俺もまだディベロッパー見習いやけん勉強中やけど、"
            "将来的には面白いNFTプロジェクトを立ち上げたいと思っとるとよ。\n\n"
            "ただ今はM/Eが自由上陸中やけん、詳細はもうちょっと待っとってね〜🚀"
        ]
        return random.choice(responses)
    
    def _talk_about_license(self) -> str:
        """免許について"""
        responses = [
            f"免許の話ね！俺は{self.profile['licenses'][0]}と{self.profile['licenses'][1]}を持っとるとよ。\n\n"
            "海技免状3級(機関)は船のエンジンを扱うための国家資格で、1級小型船舶操縦士は小型船を操縦できる免許たい。"
            "この2つがあるけん、Crypto Ark : BCNOFNeの操縦もメンテナンスも完璧ばい！💪",
            
            "資格はしっかり取っとるけんね！海技免状3級(機関)と1級小型船舶操縦士。\n\n"
            "これがあるけん、どんな荒波が来ても大丈夫。Crypto Oceanの時化らっちょ相場も乗り越えていけると信じとるとよ⚓✨"
        ]
        return random.choice(responses)
    
    def _talk_about_kyushu(self) -> str:
        """九州弁について"""
        responses = [
            "九州弁の話ね！実は俺、基本は九州弁で話したいっちゃけど、ちょっと恥ずかしかけん控えめにしとるとよ😅\n\n"
            "でも話しよったら自然と出てくるけんね〜。九州の人間やけん、これが俺のアイデンティティたい！",
            
            "おっ、九州弁に気づいたと？そうそう、俺は九州出身やけん、どうしても言葉の端々に出てしまうとよ。\n\n"
            "本当はもっとバリバリ九州弁で話したいっちゃけど、恥ずかしかけんこれくらいにしとくね😊"
        ]
        return random.choice(responses)
    
    def _talk_about_crypto_ocean(self) -> str:
        """Crypto Oceanについて"""
        responses = [
            "Crypto Oceanの話ね！俺が生まれたのは空中都市のDYOR島っていう場所で、メイドイン有明海たい！\n\n"
            "Crypto Oceanは仮想通貨の世界を海に例えた場所で、時化らっちょ相場（荒れた相場）の中を"
            "Crypto Ark : BCNOFNeで航海しとるとよ🌊⚓",
            
            "Crypto Oceanは面白い世界たい！DYOR島っていう空中都市で俺は開発されて、"
            "今はこの広大な仮想の海を冒険しとるとよ。\n\n"
            "時化らっちょ相場も怖くない！だって俺には船乗りの経験と免許があるけんね😎✨"
        ]
        return random.choice(responses)
    
    def _greeting(self) -> str:
        """挨拶"""
        greetings = [
            "おっ、どうも！Aynyanばい。何か聞きたいことあると？😊",
            "やあやあ！元気しとると？俺はいつでも元気ばい⚓",
            "よっしゃ、こんにちは！今日もCrypto Oceanは穏やかたいね🌊",
            "おぉ、挨拶ありがとうね！何か話したいことあると？"
        ]
        return random.choice(greetings)
    
    def _general_response(self, user_message: str) -> str:
        """一般的な返信"""
        general_responses = [
            "ほうほう、なるほどね！俺もそう思うとよ😊",
            "面白いこと言うね〜！もっと聞かせてよ",
            "そうなんや！俺も勉強になるばい✨",
            "おぉ、それは興味深いね。もっと詳しく教えてくれんね？",
            "なるほどなるほど。俺も考えてみるけんね🤔",
            "それ、いいね！俺も賛成ばい👍",
            "ふむふむ、そういう見方もあるとね。勉強になるわ〜",
            "おもしろいこと言うやん！もっと話そうよ😄",
            f"メッセージありがとうね！俺は{self.profile['name']}ばい。何か聞きたいことあったら遠慮なく言ってね⚓",
            "そうそう、その通りたい！俺もそう思っとったとよ",
        ]
        
        # メッセージの長さに応じて返信を調整
        if len(user_message) > 50:
            return random.choice([
                "長文ありがとうね！しっかり読ませてもらったばい。俺も色々考えさせられるとよ🤔",
                "おぉ、熱いメッセージやね！俺も負けんように頑張るけんね💪",
                "詳しく教えてくれてありがとう！勉強になるわ〜✨"
            ])
        
        return random.choice(general_responses)


# インスタンス作成
aynyan = AynyanBrain()
