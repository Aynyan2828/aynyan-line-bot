# 🔧 修正内容（v2.1）

## エラー内容
```
OpenAI API Error: Client.__init__() got an unexpected keyword argument 'proxies'
```

## 原因
OpenAI Pythonライブラリの最新バージョン（v1.x）では、初期化方法が変更されました。

## 修正内容

### aynyan_brain.py

#### 修正前（エラーが出る）
```python
import openai

openai.api_key = OPENAI_API_KEY

response = openai.chat.completions.create(...)
```

#### 修正後（正しい）
```python
from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)

response = client.chat.completions.create(...)
```

## 変更ファイル
- `aynyan_brain.py` - OpenAI クライアントの初期化方法を修正

## その他のファイル
- `config_env.py` - 変更なし
- `main.py` - 変更なし
- `requirements.txt` - 変更なし

## デプロイ方法

### GitHubを更新
1. Codespacesで `aynyan_brain.py` を開く
2. 修正版の内容に置き換える
3. コミット＆同期

### Render.comでデプロイ
1. 「Manual Deploy」→「Deploy latest commit」
2. デプロイ完了を待つ
3. LINEでテスト

## テスト方法

LINEでボットに以下を送信：

1. **キーワードテスト**
   - 「こんにちは」→ 定型文で返信（無料）
   
2. **AIテスト**
   - 「好きな食べ物は？」→ AIが佐賀弁で返信（有料）
   - 「今日の天気どう？」→ AIが返信

3. **エラーチェック**
   - Render.comのログで「OpenAI API Error」が出ないことを確認

## 修正版バージョン
v2.1 - OpenAI API初期化エラー修正版
