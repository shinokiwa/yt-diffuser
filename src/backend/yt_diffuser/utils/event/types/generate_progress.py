from enum import Enum
import multiprocessing

from yt_diffuser.utils.event.types.base_event import BaseEvent


class GenerateProgressEvent (BaseEvent):
    """
    生成進捗イベント
    """
    event_name: str = 'generate_progress'
    
    @classmethod
    def send_process(cls,
        process_queue: multiprocessing.Queue,
        *,
        generate_total: int = 0,
        generate_count: int = 0,
        steps_total: int = 0,
        steps_count: int = 0,
        percentage: float = 0,
        elapsed: float = 0,
        remaining: float = 0,
        average: float = 0
    ):
        data = {
            "generate_total": generate_total,
            "generate_count": generate_count,
            "steps_total": steps_total,
            "steps_count": steps_count,
            "percentage": percentage,
            "elapsed": elapsed,
            "remaining": remaining,
            "average": average
        }
        return super().send_process(process_queue, data)