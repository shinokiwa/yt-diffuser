import logging; logger = logging.getLogger(__name__)
import multiprocessing
from queue import Queue

from injector import inject

from .interface import IGeneratorPresenter
from yt_diffuser.types.web.event import WebEvent, WebEventType
from yt_diffuser.types.generator.message import (
    GenerateMessageResult,
    GeneratorStatus
)

class GeneratorPresenter(IGeneratorPresenter):
    """
    出力処理のためのプレゼンター
    """

    @inject
    def __init__(self):
        pass
    
    def send(self, result_queue:Queue, send_queue:multiprocessing.Queue):
        """
        出力処理のメッセージを送信する
        """
        logger.debug("Start presenting...")

        while True:
            result:GenerateMessageResult = result_queue.get()

            message = WebEvent(
                type=WebEventType.GENERATOR,
                args=result.model_dump()
            )
            send_queue.put(message.model_dump())

            if result.status == GeneratorStatus.EXIT:
                break

        logger.debug("End presenting...")
        return
    
