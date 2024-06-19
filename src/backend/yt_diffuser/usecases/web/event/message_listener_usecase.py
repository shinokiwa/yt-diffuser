import logging; logger = logging.getLogger(__name__)
import multiprocessing

from injector import inject

from yt_diffuser.stores.process.interface import IProcessQueueStore

from .event_usecase import EventUseCase

class WebMessageListenerUseCase:
    """
    Webプロセスのメッセージリスナーユースケース
    """

    @inject
    def __init__(self, process_queue_store:IProcessQueueStore, event: EventUseCase):
        self.process_queue_store = process_queue_store
        self.event = event

    def listen(self):
        """
        受信を開始する。
        """
        process_queue:multiprocessing.Queue = self.process_queue_store.get_self_queue()

        while True:
            data = process_queue.get()
            self.event.trigger(data)
