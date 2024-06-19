import logging; logger = logging.getLogger(__name__)
import multiprocessing
from queue import Queue

from injector import inject

from .interface import IGeneratorController
from yt_diffuser.usecases.generator.listen_usecase import ListenUsecase
from yt_diffuser.types.error import GeneratorExitSignal

class GeneratorController(IGeneratorController):
    """
    入力受付のためのコントローラ
    """

    @inject
    def __init__(self, usecase:ListenUsecase):
        """
        コンストラクタ
        """
        self.usecase = usecase

    def listen(self, recv_queue:multiprocessing.Queue, task_queue:Queue):
        """
        リクエストの受付を開始する
        """
        logger.debug("Start listening...")

        while True:
            try:
                self.usecase.handle(recv_queue, task_queue)
            except GeneratorExitSignal:
                break
            except Exception as e:
                logger.error(f"Error: {e}", stack_info=True)

        logger.debug("End listening...")

