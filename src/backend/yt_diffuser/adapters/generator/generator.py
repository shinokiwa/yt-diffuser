import logging; logger = logging.getLogger(__name__)
from typing import Dict
from queue import Queue

from injector import inject

from .interface import IGenerator

from yt_diffuser.usecases.generator.generator_usecase import GeneratorUseCase
from yt_diffuser.types.error import GeneratorExitSignal

class Generator(IGenerator):
    """
    生成処理メイン実行のためのアダプター
    """

    @inject
    def __init__(
        self,
        usecase:GeneratorUseCase,
    ):
        self.usecase = usecase

    def process(self, task_queue:Queue, result_queue:Queue):
        logger.debug("Start generator...")
        while True:
            try:
                self.usecase.handle(task_queue, result_queue)
            except GeneratorExitSignal:
                break
            except Exception as e:
                logger.error(f"Error: {e}", stack_info=True)

        logger.debug("End generator...")
 