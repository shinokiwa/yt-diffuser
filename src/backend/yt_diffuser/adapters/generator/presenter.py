import multiprocessing
import logging; logger = logging.getLogger(__name__)

from yt_diffuser.api.web.events.server import ServerEventData, ServerEventDataGenerateProgress, ServerEventType

class GeneratorPresenter:
    """
    出力処理のためのプレゼンター
    """

    def __init__(self, message_queue: multiprocessing.Queue):
        self.queue = message_queue
    
