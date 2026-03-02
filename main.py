"""
LINE Bot Webhook Server - AYN強化版（運用安定化）
"""
from fastapi import FastAPI, Request, HTTPException
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, ImageMessage, FileMessage, TextSendMessage
from config_env import LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET
from aynyan_brain import aynyan
import uvicorn
import requests
import os

import time
import logging
from collections import deque, defaultdict

# Pi連携用の環境変数
PI_INGEST_URL = os.getenv("PI_INGEST_URL") # 例: https://xxxxx.ts.net/ingest
PI_INGEST_KEY = os.getenv("PI_INGEST_KEY")

app = FastAPI()

# --- logging 設定（systemd/journalctlで見やすくなる） ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("aynyan")

# LINE Bot APIの初期化
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# --- 簡易レート制限（ユーザーごと） ---
# 例：10秒で6通以上なら抑制
RATE_WINDOW_SEC = 10
RATE_MAX_MSG = 6
_user_msg_times = defaultdict(deque)

# --- 重複イベント対策（LINE側の再送に備える） ---
# 直近の event_id を覚えて二重返信を防ぐ（5分保持）
_recent_event_ids = deque(maxlen=500)
_recent_event_ids_ts = {}
EVENT_ID_TTL_SEC = 300


@app.get("/")
async def root():
    """ヘルスチェック用エンドポイント"""
    return {"status": "AYN Bot is running!", "version": "Enhanced v2.1-stable"}


@app.post("/webhook")
async def webhook(request: Request):
    """
    LINE Webhookエンドポイント
    LINEからのメッセージを受信して処理する
    """
    body = await request.body()
    body_str = body.decode("utf-8")

    signature = request.headers.get("X-Line-Signature", "")

    try:
        handler.handle(body_str, signature)
    except InvalidSignatureError:
        logger.warning("Invalid signature")
        raise HTTPException(status_code=400, detail="Invalid signature")
    except Exception as e:
        # ここで落ちるとLINE側がリトライして二重返信の元になるけん、ログだけ残して200返す戦略もアリ
        logger.exception(f"Webhook handling error: {e}")
        # ただし開発中はエラー見たいならHTTP 500でもよか。運用はOK返し推奨。
        return "OK"

    return "OK"


def _is_rate_limited(user_id: str) -> bool:
    """ユーザーごとの簡易レート制限"""
    now = time.time()
    q = _user_msg_times[user_id]

    # 古い時刻を捨てる
    while q and (now - q[0] > RATE_WINDOW_SEC):
        q.popleft()

    # 今回分を追加
    q.append(now)

    return len(q) > RATE_MAX_MSG


def _is_duplicate_event(event) -> bool:
    """event_id があれば重複返信を防ぐ"""
    event_id = getattr(event, "webhook_event_id", None) or getattr(event, "event_id", None)
    if not event_id:
        return False  # 取れない環境ならスキップ

    now = time.time()

    # TTL過ぎたやつ掃除
    # dequeはmaxlenで増えすぎ防止、辞書はTTLで掃除
    expired = [eid for eid, ts in list(_recent_event_ids_ts.items()) if now - ts > EVENT_ID_TTL_SEC]
    for eid in expired:
        _recent_event_ids_ts.pop(eid, None)

    if event_id in _recent_event_ids_ts:
        return True

    _recent_event_ids.append(event_id)
    _recent_event_ids_ts[event_id] = now
    return False


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    """
    テキストメッセージを処理する（message handler）
    """
    user_id = getattr(event.source, "user_id", "unknown")
    user_message = (event.message.text or "").strip()

    # 二重返信防止
    if _is_duplicate_event(event):
        logger.info(f"[DUP] {user_id}: {user_message}")
        return

    logger.info(f"[MSG] {user_id}: {user_message}")

    # 空/超短文対策（節約）
    if not user_message:
        reply_message = "おるばい⚓（なんて言うたと？）"
    elif len(user_message) <= 1:
        reply_message = "おるばい⚓"
    else:
        # レート制限（連投時は軽量返答）
        if _is_rate_limited(user_id):
            reply_message = "連投しすぎばい⚓ 落ち着いて1つずつ言うてくれたら助かるとよ"
        else:
            try:
                reply_message = aynyan(user_message)
            except Exception as e:
                logger.exception(f"[ERROR] brain failed: {e}")
                reply_message = "機関に一瞬ノイズが走ったばい…もう一回頼む⚓"

    # 空返信ガード
    if not reply_message:
        reply_message = "すまん、応答が拾えんやった。もう一回言うてくんしゃい⚓"

    # 長文暴発防止（LINE制限＆読みやすさ）
    reply_message = reply_message[:1000]

    try:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )
        logger.info(f"[REPLY] {user_id}: {reply_message[:80]}{'…' if len(reply_message) > 80 else ''}")
    except Exception as e:
        # 返信失敗もログに残す
        logger.exception(f"[ERROR] reply_message failed: {e}")

@handler.add(MessageEvent, message=(ImageMessage, FileMessage))
def handle_media_message(event):
    """
    画像やファイル（CSV等）のメッセージを処理し、Raspberry Piに転送する
    """
    user_id = getattr(event.source, "user_id", "unknown")
    message_id = event.message.id
    
    # 二重送受信防止
    if _is_duplicate_event(event):
        logger.info(f"[DUP MEDIA] {user_id}: {message_id}")
        return

    logger.info(f"[MEDIA] {user_id}: {message_id}")

    # 拡張子・ファイル種類の判定
    filename = "image.jpg"
    is_csv = False
    
    if isinstance(event.message, FileMessage):
        filename = event.message.file_name
        if filename.lower().endswith(".csv"):
            is_csv = True
            
    # 返信制限(レート制限)等もかけられますが、ここでは簡易にACKを返します
    ack_msg = "📊 CSVデータを受け取ったばい！ラズパイに転送してOBD高精度解析を開始するけん！" if is_csv else "🔥 写真を受け取ったばい！ラズパイに転送して焼却炉OCR解析を開始するけん！"
    try:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ack_msg))
    except Exception as e:
        logger.exception(f"[ERROR] media ACK reply failed: {e}")

    # LINEからバイナリを取得してラズパイへ転送
    try:
        message_content = line_bot_api.get_message_content(message_id)
        file_binary = b""
        for chunk in message_content.iter_content():
            if chunk:
                file_binary += chunk
            
        # ラズパイ側に送る
        files = {"file": (filename, file_binary)}
        data = {
            "message_id": message_id,
            "user_id": user_id,
            "type": "obd" if is_csv else "incinerator"
        }
        headers = {"X-API-KEY": PI_INGEST_KEY}
        
        pi_res = requests.post(PI_INGEST_URL, headers=headers, files=files, data=data, timeout=30)
        pi_res.raise_for_status()
        logger.info(f"[PI TRANSFER SUCCESS] {user_id}: {message_id}")
        
    except Exception as e:
        logger.exception(f"[PI TRANSFER ERROR] {e}")
        try:
            line_bot_api.push_message(user_id, TextSendMessage(text=f"⚠️ ラズパイへの転送・解析予約に失敗したばい…Tailscaleとかの設定ば確認してね。\n{str(e)}"))
        except:
            pass

if __name__ == "__main__":
    # サーバーを起動
    uvicorn.run(app, host="0.0.0.0", port=10000)
