# Aynyan LINE Bot 🚢⚓

Crypto Ark : BCNOFNeのM/E(メインエンジン＝メガネエンジン)、Aynyanの自動返信LINEボット

## 概要

このボットは、LINE Messaging APIを使用して、受信したメッセージに対してAynyanのキャラクターになりきって自動返信します。

### Aynyanのプロフィール

- **名前**: Aynyan
- **出身**: Crypto Oceanの空中都市DYOR島（メイドイン有明海）
- **役割**: Crypto Ark : BCNOFNeの人力知能搭載M/E
- **職業**: 仮想通貨SuiのNFTクリエイター兼ファウンダー兼ディベロッパー見習い
- **経歴**: 元船乗り（機関士8年、船長見習い）、2025年引退して転職
- **免許**: 海技免状3級(機関)、1級小型船舶操縦士
- **特徴**: 九州弁が言葉の端々に出る、面白おかしく話す

## 機能

- ✅ キーワード検出による自動返信
- ✅ 自己紹介、船、NFT、免許などのトピックに対応
- ✅ Aynyanのキャラクターを反映した返信
- ✅ 九州弁を織り交ぜた自然な会話

## ファイル構成

```
aynyan_bot/
├── main.py              # FastAPIサーバー（Webhook受信）
├── aynyan_brain.py      # Aynyanの返信生成ロジック
├── config.py            # 設定ファイル（ローカル用）
├── config_env.py        # 設定ファイル（環境変数版）
├── requirements.txt     # Pythonパッケージ
├── render.yaml          # Render.com用設定
├── railway.json         # Railway用設定
├── Procfile             # Heroku互換サービス用
└── README.md            # このファイル
```

## ローカルでのテスト

### 1. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 2. サーバーの起動

```bash
python3 main.py
```

サーバーは `http://localhost:8000` で起動します。

### 3. 動作確認

```bash
curl http://localhost:8000/
```

正常に起動していれば、以下のようなレスポンスが返ります：

```json
{
  "status": "ok",
  "bot": "Aynyan LINE Bot",
  "message": "Crypto Ark : BCNOFNeのM/Eが稼働中ばい⚓"
}
```

## 24時間稼働のデプロイ方法

### オプション1: Render.com（推奨）

1. [Render.com](https://render.com)にサインアップ
2. 「New +」→「Web Service」を選択
3. GitHubリポジトリを接続（または手動でコードをアップロード）
4. 以下の設定を行う：
   - **Name**: `aynyan-line-bot`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: `Free`
5. 環境変数を設定：
   - `LINE_CHANNEL_ACCESS_TOKEN`: チャネルアクセストークン
   - `LINE_CHANNEL_SECRET`: チャネルシークレット
   - `LINE_CHANNEL_ID`: チャネルID
   - `LINE_USER_ID`: ユーザーID
6. デプロイ完了後、Webhook URLをコピー（例: `https://aynyan-line-bot.onrender.com/webhook`）

### オプション2: Railway

1. [Railway.app](https://railway.app)にサインアップ
2. 「New Project」→「Deploy from GitHub repo」を選択
3. リポジトリを選択
4. 環境変数を設定（上記と同じ）
5. デプロイ完了後、Webhook URLをコピー

### オプション3: Fly.io

1. [Fly.io](https://fly.io)にサインアップ
2. Fly CLIをインストール
3. プロジェクトディレクトリで以下を実行：

```bash
fly launch
fly secrets set LINE_CHANNEL_ACCESS_TOKEN="your_token"
fly secrets set LINE_CHANNEL_SECRET="your_secret"
fly secrets set LINE_CHANNEL_ID="your_id"
fly secrets set LINE_USER_ID="your_user_id"
fly deploy
```

## LINE Developers ConsoleでのWebhook設定

1. [LINE Developers Console](https://developers.line.biz/console/)にログイン
2. 該当のチャネルを選択
3. 「Messaging API」タブを開く
4. 「Webhook settings」セクションで以下を設定：
   - **Webhook URL**: `https://your-deployed-url.com/webhook`
   - **Use webhook**: ON
5. 「Verify」ボタンをクリックして接続をテスト
6. 「Auto-reply messages」をOFFにする（重複を避けるため）

## テスト方法

1. LINE公式アカウントを友だち追加
2. メッセージを送信してみる：
   - 「自己紹介して」→ Aynyanの詳しい自己紹介
   - 「船について教えて」→ 船乗り経験の話
   - 「NFTやってる?」→ Sui NFTプロジェクトの話（ぼかし版）
   - 「こんにちは」→ 挨拶の返信
   - その他のメッセージ → 一般的な返信

## トラブルシューティング

### Webhookが動作しない

- LINE Developers ConsoleでWebhook URLが正しく設定されているか確認
- Webhook URLの末尾が `/webhook` になっているか確認
- サーバーが正常に起動しているか確認（ヘルスチェック: `/health`）

### 返信が来ない

- サーバーログを確認
- LINE公式アカウントの「Auto-reply messages」がOFFになっているか確認
- Channel Access Tokenが正しいか確認

## カスタマイズ

### 返信内容の変更

`aynyan_brain.py` の各メソッドを編集することで、返信内容をカスタマイズできます。

### キーワードの追加

`config.py` の `KEYWORDS` 辞書に新しいキーワードを追加できます。

### キャラクター設定の変更

`config.py` の `AYNYAN_PROFILE` 辞書を編集することで、キャラクター設定を変更できます。

## ライセンス

このプロジェクトは個人用です。

## 作者

Aynyan（Crypto Ark : BCNOFNeのM/E）

---

**Crypto Oceanでも時化らっちょ相場の海を渡っていけると信じています⚓🌊**
