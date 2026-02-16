"""
Aynyan LINE Bot - Webhook Server
FastAPIを使用したLINE Messaging API Webhookサーバー
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import hashlib
import hmac
import base64
import requests
import json
from aynyan_brain import aynyan
from config import LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET

app = FastAPI(title="Aynyan LINE Bot")

LINE_REPLY_ENDPOINT = "https://api.line.me/v2/bot/message/reply"


def verify_signature(body: bytes, signature: str) -> bool:
    """LINE Webhookの署名を検証"""
    hash_digest = hmac.new(
        LINE_CHANNEL_SECRET.encode('utf-8'),
        body,
        hashlib.sha256
    ).digest()
    expected_signature = base64.b64encode(hash_digest).decode('utf-8')
    return hmac.compare_digest(signature, expected_signature)


def send_reply(reply_token: str, message_text: str):
    """LINEにメッセージを返信"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }
    
    data = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "text",
                "text": message_text
            }
        ]
    }
    
    response = requests.post(LINE_REPLY_ENDPOINT, headers=headers, json=data)
    
    if response.status_code != 200:
        print(f"Error sending reply: {response.status_code} - {response.text}")
    
    return response


@app.get("/")
async def root():
    """ヘルスチェック用エンドポイント"""
    return {
        "status": "ok",
        "bot": "Aynyan LINE Bot",
        "message": "Crypto Ark : BCNOFNeのM/Eが稼働中ばい⚓"
    }


@app.post("/webhook")
async def webhook(request: Request):
    """LINE Webhook エンドポイント"""
    # リクエストボディを取得
    body = await request.body()
    
    # 署名を検証
    signature = request.headers.get("X-Line-Signature", "")
    if not verify_signature(body, signature):
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # JSONをパース
    try:
        events = json.loads(body.decode('utf-8'))
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    # イベントを処理
    for event in events.get("events", []):
        # メッセージイベントのみ処理
        if event["type"] == "message" and event["message"]["type"] == "text":
            user_message = event["message"]["text"]
            reply_token = event["replyToken"]
            
            # Aynyanの返信を生成
            response_message = aynyan.generate_response(user_message)
            
            # 返信を送信
            send_reply(reply_token, response_message)
            
            # ログ出力
            print(f"Received: {user_message}")
            print(f"Replied: {response_message}")
    
    return JSONResponse(content={"status": "ok"})


@app.get("/health")
async def health():
    """ヘルスチェック"""
    return {"status": "healthy", "bot": "Aynyan"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
