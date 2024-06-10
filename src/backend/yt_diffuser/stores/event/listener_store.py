"""
イベントリスナーのストア
"""
from logging import getLogger; logger = getLogger(__name__)
from typing import Dict, List
import asyncio

from .interface import IEventListnerStore

class EventListenerStore(IEventListnerStore):
    """
    イベントリスナーのストア
    """

    _listeners: Dict[str, List[asyncio.Queue]] = {}
    """
    イベントリスナーのリスト
    """
    
    def get(self, event_name: str) -> List[asyncio.Queue]:
        """
        イベントリスナーのリストを取得する

        Args:
            event_name (str): イベント名

        Returns:
            list[asyncio.Queue]: リスナーキューオブジェクトのリスト
        """
        if event_name not in self._listeners:
            self.__class__._listeners[event_name] = []

        return self.__class__._listeners[event_name]

    def add(self, event_name: str, listener: asyncio.Queue):
        """
        イベントリスナーを追加する

        Args:
            event_name (str): イベント名
            listener (asyncio.Queue): リスナーキューオブジェクト

        Returns:
            None
        """
        listeners = self.get(event_name)
        listeners.append(listener)

        logger.debug(f"Add listener for {event_name}. id={id(listener)}")
    
    def remove(self, event_name: str, listener: asyncio.Queue):
        """
        イベントリスナーを削除する

        Args:
            event_name (str): イベント名
            listener (asyncio.Queue): リスナーキューオブジェクト

        Returns:
            None
        """
        listeners = self.get(event_name)

        if listener in listeners:
            listeners.remove(listener)

        if len(listeners) == 0:
            del self.__class__._listeners[event_name]

        logger.debug(f"Remove listener for {event_name}. id={id(listener)}")
