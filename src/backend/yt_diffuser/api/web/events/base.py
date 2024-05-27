"""
イベント制御 基底クラス
"""
from logging import getLogger; logger = getLogger(__name__)
from typing import Dict, List
import asyncio

from pydantic import BaseModel

class EventBase:
    """
    イベント制御 基底クラス
    """
    # イベントリスナー 継承先でもこのクラスの変数を使う
    _listeners: Dict[str, List[asyncio.Queue]] = {}

    @classmethod
    def get_listeners(cls) -> List[asyncio.Queue]:
        """
        リスナーリストを取得する。

        - イベント名が未登録の場合はリストを作成する。

        Returns:
            list[queue.Queue]: リスナーキューオブジェクトのリスト

        """
        if cls.__name__ not in EventBase._listeners:
            EventBase._listeners[cls.__name__] = []

        return EventBase._listeners[cls.__name__]

    @classmethod
    def get_event_listener(cls) -> asyncio.Queue:
        """
        イベントのリスナーキューを作成し、取得する。

        Args:
            event_name (str): イベント名

        Returns:
            queue.Queue: リスナーキューオブジェクト

        """
        listeners = cls.get_listeners()

        q = asyncio.Queue()
        listeners.append(q)

        logger.debug(f"Add listener for {cls.__name__}. id={id(q)}")
        return q

    @classmethod
    def remove_event_listener(cls, listener: asyncio.Queue):
        """
        リスナーキューを削除する。

        - 未登録のイベント名、リスナーキューの場合は何もしない。

        Args:
            listener (queue.Queue): 削除するリスナーキュー

        Returns:
            None
        """
        listeners = cls.get_listeners()

        if listener in listeners:
            listeners.remove(listener)

        if len(listeners) == 0:
            del EventBase._listeners[cls.__name__]

        logger.debug(f"Remove listener for {cls.__class__.__name__}. id={id(listener)}")

    @classmethod
    def send_event(cls, data = None) -> None:
        """
        イベントリスナーにイベントを配信する。

        args:
            data (dict): イベントデータ
        """
        listeners = cls.get_listeners()

        for listener in listeners:

            logger.debug(f"Put message to listener. id={id(listener)}")
            _data = data.copy() if type(data) == dict else data
            listener.put_nowait(_data)
    
    @classmethod
    def trigger(cls, data = None) -> None:
        """
        イベントをトリガーする。
        各イベントはこれをオーバーライドして実装する。

        args:
            data: イベントデータ 必要に応じて型を指定する
        """
        cls.send_event(data = data)