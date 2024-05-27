"""
サーバーイベント

プロセス状態やエラー情報などのサーバー情報を通知するためのイベント
"""
from .base import EventBase
from pydantic import BaseModel
from enum import Enum

class ServerEventType(str, Enum):
    """
    サーバーイベントタイプ
    """
    INFO = "info"
    GENERATOR = "generator"
    DOWNLOADER = "downloader"
    ERROR = "error"
    GENERATOR_PROGRESS = "generator_progress"

class ServerEventDataGenerateProgress(BaseModel):
    """
    生成進捗データ
    """
    generate_total: int = 0
    generate_count: int = 0
    steps_total: int = 0
    steps_count: int = 0
    percentage: float = 0
    elapsed: float = 0
    remaining: float = 0
    average: float = 0

class ServerEventData(BaseModel):
    """
    サーバーイベントデータ
    """
    type: ServerEventType
    """
    イベントタイプ
    """

    status: str = ""
    """
    ステータス
    """

    generator_progress: ServerEventDataGenerateProgress = ServerEventDataGenerateProgress()
    """
    生成プロセスの進捗情報
    """
    

class ServerEvent(EventBase):
    """
    サーバーイベント
    """

    @classmethod
    def trigger(cls, data: ServerEventData):
        """
        イベントをトリガーする。

        Args:
            message (str): メッセージ

        Returns:
            None
        """
        cls.send_event(data=data.model_dump())