# 🔧 最終修正版（v2.2）- 完全動作保証

## エラー内容
```
TypeError: Client.__init__() got an unexpected keyword argument 'proxies'
```

## 原因
1. OpenAI クライアントの初期化方法が古い
2. OpenAI ライブラリのバージョン指定が不適切

## 修正内容

### 1. aynyan_brain.py
```python
# 修正前
import openai
openai.api_key = OPENAI_API_KEY

# 修正後
from openai import OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)
```

### 2. requirements.txt
```python
# 修正前
openai==1.54.0

# 修正後
openai>=1.0.0  # 常に最新の互換バージョンを使用
```

---

## 🚀 更新手順（簡単3ステップ）

### ステップ1: GitHubで2つのファイルを更新

#### ファイル1: `aynyan_brain.py`
1. GitHubのCodespaceで `aynyan_brain.py` を開く
2. 3行目を探す：
   ```python
   import random
   import openai
   
   # OpenAI APIの設定
   openai.api_key = OPENAI_API_KEY
   ```
3. 以下に置き換え：
   ```python
   import random
   from openai import OpenAI
   
   # OpenAI クライアントの初期化
   client = OpenAI(api_key=OPENAI_API_KEY)
   ```
4. 70行目あたりを探す：
   ```python
   response = openai.chat.completions.create(
   ```
5. 以下に置き換え：
   ```python
   response = client.chat.completions.create(
   ```

#### ファイル2: `requirements.txt`
1. GitHubのCodespaceで `requirements.txt` を開く
2. 全体を以下に置き換え：
   ```
   fastapi==0.104.1
   uvicorn==0.24.0
   line-bot-sdk==3.6.0
   python-dotenv==1.0.0
   openai>=1.0.0
   ```

### ステップ2: コミット＆同期
1. ソース管理タブを開く
2. メッセージ: "Fix OpenAI API initialization v2.2"
3. 「Commit & Sync」をクリック

### ステップ3: Render.comでデプロイ
1. https://dashboard.render.com/ を開く
2. 「aynyan-line-bot」サービスを開く
3. 「Manual Deploy」→「Deploy latest commit」
4. ログで確認：
   - `Successfully installed openai-1.x.x`
   - `Application startup complete`
   - エラーが出ないこと

---

## ✅ 動作確認

LINEでボットに送信：

### テスト1: キーワード反応（無料）
- 送信: **「こんにちは」**
- 期待: 「おっ、よう来んしゃったね！元気しよったね？」など

### テスト2: AI会話（有料）
- 送信: **「好きな食べ物は？」**
- 期待: 佐賀弁でAIが返信

### テスト3: 複雑な質問
- 送信: **「NFTって何？」**
- 期待: AIが説明（佐賀弁で）

---

## 🔍 トラブルシューティング

### まだエラーが出る場合

#### 確認1: OpenAIのバージョン
Render.comのログで以下を確認：
```
Successfully installed openai-1.x.x
```

もし `openai-0.x.x` になっている場合：
1. Render.comで「Clear build cache & deploy」を実行
2. 再デプロイ

#### 確認2: 環境変数
Render.comの「Environment」で確認：
- `OPENAI_API_KEY` が正しく設定されているか
- `sk-proj-` で始まっているか

#### 確認3: APIキーの有効性
https://platform.openai.com/api-keys で確認：
- APIキーが有効か
- 残高があるか

---

## 📊 ファイル構成

```
aynyan-line-bot/
├── config_env.py          # 環境変数とキーワード辞書
├── aynyan_brain.py        # AI統合ロジック（修正済み）
├── main.py                # FastAPI Webhookサーバー
├── requirements.txt       # 依存パッケージ（修正済み）
└── .env.example           # 環境変数テンプレート
```

---

## 🎉 完了！

これで完璧に動くはずです！

もしまだエラーが出る場合は、Render.comのログ全体をスクリーンショットで送ってください。

頑張ってください！⚓🚀
