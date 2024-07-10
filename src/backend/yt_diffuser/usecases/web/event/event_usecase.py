import logging; logger = logging.getLogger(__name__)
from typing import Dict
import asyncio

from injector import inject

from yt_diffuser.types.web.event import WebEvent, WebEventType
from yt_diffuser.stores.event.interface import IEventListnerStore

class EventUseCase:
    """
    サーバーイベント処理のユースケース

    送受信どちらからも使用できる。
    """

    @inject
    def __init__(self, store: IEventListnerStore):
        self.store = store
    
    def get_listener(self, key:WebEventType)-> asyncio.Queue:
        """
        イベントリスナーを新規に作成して取得する。

        Returns:
            None
        """
        listener = asyncio.Queue()
        self.store.add(key.value, listener)
        return listener
    
    def trigger(self, data: Dict):
        """
        イベントリスナーにイベントを配信する。

        args:
            data (ServerEventData): イベントデータ
        """
        event = WebEvent(**data)

        listeners = self.store.get(event.type.value)

        for listener in listeners:

            listener.put_nowait(event.args)
        
    def remove_listener(self, key:WebEventType, listener: asyncio.Queue):
        """
        イベントリスナーを削除する。

        args:
            listener (asyncio.Queue): イベントリスナー
        """
        self.store.remove(key.value, listener)
