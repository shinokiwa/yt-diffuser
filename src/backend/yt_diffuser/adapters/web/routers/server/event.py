"""
サーバーイベントを受信するためのSSE(Server-Sent Events)
"""
import asyncio
from logging import getLogger; logger = getLogger(__name__)

from fastapi import APIRouter, Request, Depends
from fastapi.responses import StreamingResponse

from yt_diffuser.injector import get_depends
from yt_diffuser.usecases.web.event.server_event_usecase import (
    ServerEventUseCase,
    ServerEventData,
    ServerEventDataGenerateProgress
)

router = APIRouter()

@router.get("/api/server/event")
async def get_server_message(request: Request, usecase:ServerEventUseCase = Depends(get_depends(ServerEventUseCase))):
    """
    サーバーイベントを受信するためのSSE(Server-Sent Events)

    Args:
        request (Request): リクエスト

    Returns:
        StreamingResponse: サーバーイベントのストリーム
    """
    # 新しいクライアントのためのキューを作成
    queue = usecase.get_listener()
    
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
        usecase.remove_listener(queue)
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")