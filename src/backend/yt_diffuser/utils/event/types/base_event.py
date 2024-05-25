"""
イベントの基底
"""
import multiprocessing

from yt_diffuser.utils.event.listener import (
    get_event_listener,
    remove_event_listener,
    send_event
)

class BaseEvent:
    """
    イベントの基底クラス
    """
    event_name: str = None
    cache: bool = True

    @classmethod
    def get_listener(cls):
        """
        イベントリスナーを取得する。
        """
        return get_event_listener(cls.event_name)

    @classmethod
    def remove_listener(cls, listener):
        """
        イベントリスナーを削除する。
        """
        remove_event_listener(cls.event_name, listener)
    
    @classmethod
    def send(cls, data: dict | None = None):
        """
        イベントを送信する。
        """
        send_event(cls.event_name, cls.cache, data)
    
    @classmethod
    def send_process(cls, process_queue:multiprocessing.Queue, data: dict | None = None):
        """
        別プロセスにイベントを送信する。
        """
        process_queue.put((cls.event_name, cls.cache, data))

