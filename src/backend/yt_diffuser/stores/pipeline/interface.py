from abc import ABCMeta, abstractmethod

from diffusers import DiffusionPipeline


class IPipelineStore(metaclass=ABCMeta):
    """
    パイプラインストアのインターフェース

    パイプラインのシングルトン化を行うためのストア。
    """

    @abstractmethod
    def set_pipeline(self, pipeline:DiffusionPipeline) -> None:
        """
        パイプラインをストックする。

        Args:
            pipeline (DiffusionPipeline): パイプライン
        """
        pass

    @abstractmethod
    def get_pipeline(self) -> DiffusionPipeline | None:
        """
        パイプラインを取得する。
        存在しない場合はNoneを返す。

        Returns:
            DiffusionPipeline: パイプライン
        """
        pass

    @abstractmethod
    def clear_pipeline(self) -> None:
        """
        パイプラインをクリアする。
        """
        pass
