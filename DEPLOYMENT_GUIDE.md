# AYN強化版 デプロイガイド

## 🚀 強化内容

### 1. キーワード反応の大幅拡充
以下のカテゴリに対応：
- 挨拶（こんにちは、おはよう、など）
- 感謝（ありがとう、など）
- 謝罪（ごめん、すみません、など）
- 自己紹介
- Sui/NFT/Crypto関連
- 船・海関連
- 佐賀弁について
- 元気・調子
- 好き・嫌い・趣味
- 天気
- 励まし・応援
- 疲れた・大変
- 笑い・面白い

### 2. AI会話統合（OpenAI GPT-4o mini）
- キーワードに当てはまらない質問にも自然に返答
- 佐賀弁を維持しながら柔軟な対話
- 文脈を理解した返信

### 3. 感情・状況分析
- ポジティブ/ネガティブ/質問/雑談を自動判定
- 状況に応じた適切なトーンで返信

---

## 📋 必要なもの

1. **LINE Messaging API**
   - Channel Access Token
   - Channel Secret

2. **OpenAI API Key**（新規）
   - https://platform.openai.com/api-keys で取得
   - GPT-4o mini使用（月額約24円程度）

3. **Render.comアカウント**
   - 既存のサービスを使用

---

## 🔧 デプロイ手順

### Step 1: OpenAI API Keyを取得

1. https://platform.openai.com/ にアクセス
2. アカウント作成/ログイン
3. 「API Keys」から新しいキーを作成
4. キーをコピー（`sk-proj-...`で始まる文字列）

### Step 2: GitHubリポジトリを更新

#### 方法A: GitHub Codespaces（推奨）

1. GitHubリポジトリ（Aynyan2828/aynyan-line-bot）を開く
2. 「Code」→「Codespaces」→「Create codespace on main」
3. 既存のファイルを削除：
   - `config_env.py`
   - `aynyan_brain.py`
   - `main.py`
   - `requirements.txt`
4. 新しいファイルをアップロード：
   - `ayn_enhanced.zip`を解凍
   - すべてのファイルをドラッグ&ドロップ
5. ソース管理から変更をコミット：
   - メッセージ: "Enhanced AYN with AI integration"
   - 「Commit & Sync」をクリック

#### 方法B: ローカルGit

```bash
# リポジトリをクローン
git clone https://github.com/Aynyan2828/aynyan-line-bot.git
cd aynyan-line-bot

# 古いファイルを削除
rm config_env.py aynyan_brain.py main.py requirements.txt

# 新しいファイルをコピー
cp /path/to/ayn_enhanced/* .

# コミット＆プッシュ
git add .
git commit -m "Enhanced AYN with AI integration"
git push origin main
```

### Step 3: Render.comで環境変数を追加

1. https://dashboard.render.com/ にアクセス
2. 「aynyan-line-bot」サービスを開く
3. 左メニューから「Environment」をクリック
4. 「Add Environment Variable」をクリック
5. 以下を追加：
   ```
   Key: OPENAI_API_KEY
   Value: sk-proj-... (取得したAPIキー)
   ```
6. 「Save Changes」をクリック

### Step 4: デプロイ

1. Render.comのダッシュボードで「Manual Deploy」をクリック
2. 「Deploy latest commit」を選択
3. デプロイが完了するまで待つ（3-5分）
4. ログで「Application startup complete」を確認

### Step 5: 動作確認

1. LINEでボットにメッセージを送信
2. 以下をテスト：
   - 挨拶: 「こんにちは」→ 定型文で即座に返信
   - 質問: 「好きな食べ物は？」→ AIが佐賀弁で返信
   - 複雑な質問: 「NFTって何？」→ AIが説明
   - 励まし: 「頑張って」→ 感情を理解して返信

---

## 💰 コスト試算

### OpenAI API（GPT-4o mini）
- **料金**: $0.150/1M入力トークン、$0.600/1M出力トークン
- **1回の会話**: 約0.01〜0.03円
- **月間1000メッセージ**: 約10〜30円
- **月間3000メッセージ**: 約30〜90円

### Render.com
- **無料プラン**: $0/月（現状維持）

### 合計
- **月額約30〜100円程度**（使用量による）

---

## 🔍 トラブルシューティング

### ボットが返信しない
1. Render.comのログを確認
2. 環境変数が正しく設定されているか確認
3. OpenAI API Keyが有効か確認

### AI返信が遅い
- GPT-4o miniは通常1-2秒で返信します
- 遅い場合はOpenAIのステータスページを確認

### エラーメッセージ: "OpenAI API Error"
1. API Keyが正しいか確認
2. OpenAIアカウントに残高があるか確認
3. API使用制限に達していないか確認

### キーワード反応が優先される
- これは正常な動作です（コスト削減のため）
- よく聞かれる質問は定型文で返信
- 複雑な質問だけAIを使用

---

## 📊 モニタリング

### Render.comログ
- リアルタイムでボットの動作を確認
- エラーやAPI呼び出しを監視

### OpenAI Usage
- https://platform.openai.com/usage
- API使用量とコストを確認

---

## 🎯 今後の拡張案

1. **会話履歴の記憶**
   - データベースを追加して過去の会話を記憶
   - より文脈に沿った返信

2. **画像対応**
   - GPT-4oを使用して画像を理解
   - 画像付きメッセージに返信

3. **スケジュール機能**
   - 定期的なメッセージ送信
   - リマインダー機能

4. **グループチャット対応**
   - 複数人での会話に対応
   - メンション機能

---

## 📝 ファイル構成

```
aynyan-line-bot/
├── config_env.py          # 環境変数とキーワード辞書
├── aynyan_brain.py        # AI統合メインロジック
├── main.py                # FastAPI Webhookサーバー
├── requirements.txt       # Python依存パッケージ
├── .env.example           # 環境変数テンプレート
└── DEPLOYMENT_GUIDE.md    # このファイル
```

---

## ✅ チェックリスト

- [ ] OpenAI API Keyを取得
- [ ] GitHubリポジトリを更新
- [ ] Render.comで環境変数を追加
- [ ] デプロイ実行
- [ ] 動作確認（挨拶、質問、複雑な質問）
- [ ] OpenAI使用量を確認

---

おめでとうございます！AYNが最強のメガネエンジンbotに進化しました！⚓🚀
