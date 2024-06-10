"""
イベントリスナーストアのインターフェース
"""
from typing import List
from abc import ABCMeta, abstractmethod
import asyncio

class IEventListnerStore(metaclass=ABCMeta):
    """
    イベントリスナーストアのインターフェース
    """

    @abstractmethod
    def get(self, event_name: str) -> List[asyncio.Queue]:
        """
        イベントリスナーのリストを取得する
        """
        pass

    @abstractmethod
    def add(self, event_name: str, listner: asyncio.Queue):
        """
        イベントリスナーを追加する
        """
        pass

    @abstractmethod
    def remove(self, event_name: str, listner: asyncio.Queue):
        """
        イベントリスナーを削除する
        """
        pass
