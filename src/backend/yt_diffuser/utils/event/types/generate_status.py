from enum import Enum
import multiprocessing

from yt_diffuser.utils.event.types.base_event import BaseEvent


class GenerateStatusEvent (BaseEvent):
    """
    生成ステータスイベント
    """
    event_name: str = 'generator'

    class Status (Enum):
        """
        生成ステータス
        """
        EXIT = 'exit'
        LOADING = 'loading'
        READY = 'ready'
        GENERATING = 'generating'
        ERROR = 'error'
    
    @classmethod
    def send_process(cls, process_queue: multiprocessing.Queue, status: Status, label: str = "", error: str = ""):
        data = {'status': status.value, 'label': label, 'error': error}
        return super().send_process(process_queue, data)