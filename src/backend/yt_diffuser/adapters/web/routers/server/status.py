"""
サーバーのステータスを取得する
"""
from logging import getLogger; logger = getLogger(__name__)

from fastapi import APIRouter
from pydantic import BaseModel

from yt_diffuser.types.web.response import ResponseModel, ResponseMeta

router = APIRouter()

class ServerStatusOutput(BaseModel):
    """
    サーバーステータスレスポンス
    """
    health: str
    downloader: str
    generator: str

@router.get("/api/server/status", response_model=ResponseModel[ServerStatusOutput])
def get_server_status():
    """
    現在のサーバーのステータスを取得する

    Returns:
        dict: サーバーのステータス
    """
    logger.debug("Get server status")

    response = ResponseModel[ServerStatusOutput](
        meta=ResponseMeta(),
        data=ServerStatusOutput(
            health="ok",
            downloader="idle",
            generator="idle"
        )
    )
    return response