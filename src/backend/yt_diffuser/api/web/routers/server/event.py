"""
サーバーイベントを受信するためのSSE(Server-Sent Events)
"""
import asyncio
from logging import getLogger; logger = getLogger(__name__)

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from ...events.server import ServerEvent, ServerEventData

router = APIRouter()

@router.get("/api/server/event")
async def get_server_message(request: Request):
    """
    サーバーイベントを受信するためのSSE(Server-Sent Events)

    Args:
        request (Request): リクエスト

    Returns:
        StreamingResponse: サーバーイベントのストリーム
    """
    # 新しいクライアントのためのキューを作成
    queue = ServerEvent.get_event_listener()
    
    async def event_generator():
        while True:
            try:
                # クライアントが接続を解除したかどうかをチェック
                if await request.is_disconnected():
                    break
                # キューからメッセージを取得
                message = await asyncio.wait_for(queue.get(), timeout=5)
                response = f"data: {message}\n\n"
            except asyncio.TimeoutError:
                response = ": keep-alive\n\n"
            except asyncio.CancelledError:
                break

            yield response


        # クライアントのキューをリストから削除
        ServerEvent.remove_event_listener(queue)
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")