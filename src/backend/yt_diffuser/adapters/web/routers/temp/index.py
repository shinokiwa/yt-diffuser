import logging; logger = logging.getLogger(__name__)
from typing import List, Union
import asyncio

from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from yt_diffuser.injector import get_depends
from yt_diffuser.types.web.response import ResponseModel, ResponseMeta
from yt_diffuser.usecases.web.tempimage.tempimage_usecase import TempImageUseCase
from yt_diffuser.usecases.web.event.event_usecase import EventUseCase, WebEventType

router = APIRouter()

class ResponseData(BaseModel):
    """
    レスポンスデータ(通常)
    """
    list: List[str] = []

class StreamData(BaseModel):
    """
    レスポンスデータ(SSE)
    """
    event_type: str = ""
    filename: str = ""

@router.get('/api/temp/', response_model=ResponseModel[ResponseData])
async def get_temp_index (
    request: Request,
    temp_image:TempImageUseCase = Depends(get_depends(TempImageUseCase)),
    event:EventUseCase = Depends(get_depends(EventUseCase))
) -> Union[ResponseModel[ResponseData], StreamingResponse]:
    """
    一時保存画像の一覧を取得する。
    リクエストのAcceptヘッダーがtext/event-streamの場合はSSE(Server-Sent Events)として返す。
    """
    accept = request.headers.get('Accept', None)

    if accept == 'text/event-stream':
        # 新しいクライアントのためのキューを作成
        queue = event.get_listener(WebEventType.TEMPFILE)
        
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
                    data = StreamData(**message)
                    response = f"data: {data.model_dump_json()}\n\n"
                except asyncio.TimeoutError:
                    response = ": keep-alive\n\n"
                except asyncio.CancelledError:
                    break

                yield response

            # クライアントのキューをリストから削除
            event.remove_listener(WebEventType.GENERATOR, queue)
        
        return StreamingResponse(event_generator(), media_type="text/event-stream")
    
    else:
        list = temp_image.get_index()
        return ResponseModel[ResponseData](
            meta=ResponseMeta(),
            data=ResponseData(list=list)
        )
