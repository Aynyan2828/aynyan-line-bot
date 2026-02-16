"""
Aynyan LINE Bot - Webhook Server
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import hashlib
import hmac
import base64
import requests
from aynyan_brain import aynyan
from config_env import LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET

app = FastAPI()

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
    """LINE Webhookエンドポイント"""
    # 署名検証
    signature = request.headers.get("X-Line-Signature")
    body = await request.body()
    
    if not verify_signature(body, signature):
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # イベント処理
    events = (await request.json()).get("events", [])
    
    for event in events:
        if event["type"] == "message" and event["message"]["type"] == "text":
            reply_token = event["replyToken"]
            user_message = event["message"]["text"]
            
            # Aynyanの返信を生成
            reply_message = aynyan(user_message)
            
            # LINE APIで返信
            send_reply(reply_token, reply_message)
    
    return JSONResponse(content={"status": "ok"})

def verify_signature(body: bytes, signature: str) -> bool:
    """LINE署名を検証"""
    hash_digest = hmac.new(
        LINE_CHANNEL_SECRET.encode("utf-8"),
        body,
        hashlib.sha256
    ).digest()
    
    expected_signature = base64.b64encode(hash_digest).decode("utf-8")
    return signature == expected_signature

def send_reply(reply_token: str, message: str):
    """LINEに返信メッセージを送信"""
    url = "https://api.line.me/v2/bot/message/reply"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }
    data = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        print(f"Error sending reply: {response.text}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
