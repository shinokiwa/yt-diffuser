from typing import Dict
from abc import ABCMeta, abstractmethod

from diffusers import DiffusionPipeline

class IPipelineUseCase (metaclass=ABCMeta):
    """
    パイプライン実行処理ユースケースのインターフェース
    """

    @abstractmethod
    def forward(self, input_data: Dict) -> None:
        """
        パイプラインを実行する

        Args:
            pipeline (DiffusionPipeline): パイプライン
            input_data (dict): 入力データ
        """
        pass