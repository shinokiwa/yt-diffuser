from typing import Tuple

from injector import inject
from diffusers.pipelines import (
    DiffusionPipeline,
    StableDiffusionXLPipeline
)

from yt_diffuser.types.path import AppPath
from yt_diffuser.types.generator import GenerateType
from yt_diffuser.stores.pipeline.interface import IPipelineStore

from .pipeline import (
    IPipelineUseCase,
    StableDiffusionXLTextToImageUseCase
)

class UseCaseSelector:
    """
    ユースケースを選択するクラス
    """

    @inject
    def __init__(
        self,
        path:AppPath,
        pipeline_store:IPipelineStore
    ) -> None:
        """
        コンストラクタ

        Args:
            path (AppPath): アプリケーションパス
            pipeline_store (IPipelineStore): パイプラインストア
        """
        self.path = path
        self.pipeline_store = pipeline_store

    def create_usecase(self, generate_type:GenerateType) -> IPipelineUseCase:
        """
        現在ストックされているパイプラインに対応するユースケースを取得する

        Args:
            generate_type (GenerateType): 生成タイプ
        """
        pipeline = self.pipeline_store.get_pipeline()

        usecase = None
        if isinstance(pipeline, StableDiffusionXLPipeline):
            if generate_type == GenerateType.TEXT_TO_IMAGE:
                usecase = StableDiffusionXLTextToImageUseCase(self.path, pipeline)
        
        return usecase
