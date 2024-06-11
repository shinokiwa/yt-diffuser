import logging; logger = logging.getLogger(__name__)
import multiprocessing

from injector import inject

from yt_diffuser.types.error import GeneratorExitSignal, ErrorMessageSignal
from yt_diffuser.types.generator import (
    GeneratorMessage,
    GeneratorMessageType,
    GenerateType
)
from yt_diffuser.usecases.generator import (
    GeneratorLoadUseCase,
    GeneratorExecuteUseCase,
    UseCaseSelector
)

class GeneratorController:
    """
    入力受付のためのコントローラ
    """

    @inject
    def __init__(
        self,
        load:GeneratorLoadUseCase,
        execute:GeneratorExecuteUseCase,
        selector:UseCaseSelector
    ):
        self.load = load
        self.execute = execute
        self.selector = selector

    def main_loop(self, recv_queue:multiprocessing.Queue, send_queue:multiprocessing.Queue):
        """
        メインループ
        """
        while True:
            try:
                data = recv_queue.get()
                message = GeneratorMessage(**data)
                self.handle(message, send_queue)
            except ErrorMessageSignal as e:
                pass
            except GeneratorExitSignal:
                logger.debug("Exit signal received")
                break
            except Exception as e:
                logger.error(f"Error: {e}", stack_info=True)
                break
    
    def handle(self, message:GeneratorMessage, queue:multiprocessing.Queue):
        """
        入力データをもとにユースケースを呼び出す
        """
        if message.message_type == GeneratorMessageType.EXIT:
            raise GeneratorExitSignal()

        elif message.message_type == GeneratorMessageType.LOAD:
            self.load.load(message.data)
        
        elif message.message_type == GeneratorMessageType.TEXT_TO_IMAGE:
            usecase = self.selector.create_usecase(GenerateType.TEXT_TO_IMAGE)
            self.execute.forward(usecase, message.data)
