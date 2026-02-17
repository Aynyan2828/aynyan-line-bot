"""
LINE Bot Webhook Server - AYN強化版
"""
from fastapi import FastAPI, Request, HTTPException
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from config_env import LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET
from aynyan_brain import aynyan
import uvicorn

app = FastAPI()

# LINE Bot APIの初期化
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


@app.get("/")
async def root():
    """ヘルスチェック用エンドポイント"""
    return {"status": "AYN Bot is running!", "version": "Enhanced v2.0"}


@app.post("/webhook")
async def webhook(request: Request):
    """
    LINE Webhookエンドポイント
    LINEからのメッセージを受信して処理する
    """
    # リクエストボディを取得
    body = await request.body()
    body_str = body.decode('utf-8')
    
    # 署名を検証
    signature = request.headers.get('X-Line-Signature', '')
    
    try:
        handler.handle(body_str, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    """
    テキストメッセージを処理する
    """
    # 受信メッセージ
    user_message = event.message.text
    
    # AYNの返信を生成
    reply_message = aynyan(user_message)
    
    # 返信を送信
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    )


if __name__ == "__main__":
    # サーバーを起動
    uvicorn.run(app, host="0.0.0.0", port=10000)
