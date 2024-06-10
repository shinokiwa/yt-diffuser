"""
サーバーイベント処理のユースケース
"""
from typing import List
import logging; logger = logging.getLogger(__name__)
import asyncio

from injector import inject
from pydantic import BaseModel
from enum import Enum

from yt_diffuser.stores.event.interface import IEventListnerStore

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

class ServerEventUseCase:
    """
    サーバーイベント処理のユースケース
    """

    @inject
    def __init__(self, store: IEventListnerStore):
        self.store = store
    
    def get_listener(self)-> asyncio.Queue:
        """
        イベントリスナーを新規に作成して取得する。

        Returns:
            None
        """
        listener = asyncio.Queue()
        self.store.add("server", listener)
        return listener
    
    def trigger(self, data: ServerEventData):
        """
        イベントリスナーにイベントを配信する。

        args:
            data (ServerEventData): イベントデータ
        """
        listeners = self.store.get("server")

        for listener in listeners:

            logger.debug(f"Put message to listener. id={id(listener)}")
            _data = data.model_dump()
            listener.put_nowait(_data)
        
    def remove_listener(self, listener: asyncio.Queue):
        """
        イベントリスナーを削除する。

        args:
            listener (asyncio.Queue): イベントリスナー
        """
        self.store.remove("server", listener)
