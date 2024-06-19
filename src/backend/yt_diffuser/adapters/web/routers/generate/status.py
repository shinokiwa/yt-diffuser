"""
サーバーイベントを受信するためのSSE(Server-Sent Events)
"""
import asyncio
from logging import getLogger; logger = getLogger(__name__)

from fastapi import APIRouter, Request, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from yt_diffuser.injector import get_depends
from yt_diffuser.usecases.web.event.event_usecase import EventUseCase, WebEventType
from yt_diffuser.types.generator.message import GeneratorStatus

class ResponseData(BaseModel):
    """
    レスポンスデータ
    """
    status: GeneratorStatus = GeneratorStatus.IDLE

    base_model_id:str = ""
    file_name:str = ""

    generate_total: int = 0
    generate_count: int = 0
    steps_total: int = 0
    steps_count: int = 0
    percentage: float = 0
    elapsed: float = 0
    remaining: float = 0
    average: float = 0

router = APIRouter()

@router.get("/api/generate/status")
async def get_server_status(request: Request, usecase:EventUseCase = Depends(get_depends(EventUseCase))):
    """
    生成ステータスイベントを受信するためのSSE(Server-Sent Events)

    Args:
        request (Request): リクエスト

    Returns:
        StreamingResponse: サーバーイベントのストリーム
    """
    # 新しいクライアントのためのキューを作成
    queue = usecase.get_listener(WebEventType.GENERATOR)
    
    async def event_generator():
        # 最初の一回は接続確認のためすぐにレスポンスを返す
        yield ": keep-alive\n\n"
        while True:
            try:
                # クライアントが接続を解除したかどうかをチェック
                if await request.is_disconnected():
                    break
                # キューからメッセージを取得
                message = await asyncio.wait_for(queue.get(), timeout=5)
                data = ResponseData(**message)
                response = f"data: {data.model_dump_json()}\n\n"
            except asyncio.TimeoutError:
                response = ": keep-alive\n\n"
            except asyncio.CancelledError:
                break

            yield response


        # クライアントのキューをリストから削除
        usecase.remove_listener(WebEventType.GENERATOR, queue)
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")