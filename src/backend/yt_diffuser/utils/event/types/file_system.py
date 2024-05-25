from enum import Enum
import multiprocessing

from yt_diffuser.utils.event.types.base_event import BaseEvent


class FilesystemEvent (BaseEvent):
    """
    ファイルシステムイベント
    """
    event_name: str = 'filesystem'
    cache: bool = False

    class Type (Enum):
        """
        イベントタイプ
        """
        EXIST = 'exist'
        CREATE = 'create'
        DELETE = 'delete'
        MODIFY = 'modify'

    @classmethod
    def send(cls, type: Type, target: str):
        """
        イベントを送信する。
        """
        data = {'type': type.value, 'target': target}
        super().send(data)
    
    @classmethod
    def send_process(cls, process_queue:multiprocessing.Queue, type: Type, target: str):
        """
        別プロセスにイベントを送信する。
        """
        data = {'type': type.value, 'target': target}
        super().send_process(process_queue, data)