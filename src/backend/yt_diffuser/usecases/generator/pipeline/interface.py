from typing import Dict
from abc import ABCMeta, abstractmethod

from queue import Queue

from yt_diffuser.types.generator.message import GenerateMessage

class IPipelineUseCase (metaclass=ABCMeta):
    """
    パイプライン実行処理ユースケースのインターフェース
    """

    @abstractmethod
    def forward(self, task:GenerateMessage, result_queue: Queue) -> None:
        """
        パイプラインを実行する

        Args:
            pipeline (DiffusionPipeline): パイプライン
            input_data (dict): 入力データ
        """
        pass