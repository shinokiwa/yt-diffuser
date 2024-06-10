from diffusers import DiffusionPipeline

from .interface import IPipelineStore

class PipelineStore(IPipelineStore):
    """
    パイプラインストア
    """

    pipeline = None

    def __init__(self):
        """
        コンストラクタ
        """
        pass

    def set_pipeline(self, pipeline:DiffusionPipeline) -> None:
        """
        パイプラインをストックする。

        Args:
            pipeline (DiffusionPipeline): パイプライン
        """
        self.__class__.pipeline = pipeline

    def get_pipeline(self) -> DiffusionPipeline | None:
        """
        パイプラインを取得する。
        存在しない場合はNoneを返す。

        Returns:
            DiffusionPipeline: パイプライン
        """
        return self.__class__.pipeline

    def clear_pipeline(self) -> None:
        """
        パイプラインをクリアする。
        """
        self.__class__.pipeline = None