from enum import Enum
import multiprocessing

from yt_diffuser.utils.event.types.base_event import BaseEvent


class DownloadStatusEvent (BaseEvent):
    """
    ダウンロードステータスイベント
    """
    event_name: str = 'download'

    class Status (Enum):
        """
        ダウンロードステータス
        """
        EMPTY = 'empty'
        START = 'start'
        DOWNLOADING = 'download'
        COMPLETE = 'complete'
        ERROR = 'error'
    
    @classmethod
    def send_process(cls, process_queue: multiprocessing.Queue, status: Status, *,
        model_name: str = "",
        revision: str = "",
        total: int = 0,
        progress: int = 0,
        percentage: float = 0,
        elapsed: float = 0,
        remaining: float = 0,
        error: str = ""
    ):
        data = {
            'status': status.value,
            'model_name': model_name,
            'revision': revision,
            'total': total,
            'progress': progress,
            'percentage': percentage,
            'elapsed': elapsed,
            'remaining': remaining,
            'error': error
        }
        return super().send_process(process_queue, data)