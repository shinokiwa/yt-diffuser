from queue import Queue

from injector import inject
from diffusers.pipelines import (
    DiffusionPipeline,
    StableDiffusionXLPipeline
)

from yt_diffuser.types.path import AppPath
from yt_diffuser.stores.pipeline.interface import IPipelineStore
from yt_diffuser.stores.generator.interface import IGeneratorStatusStore

from .pipeline import (
    PipelineUtilUseCase,
    StableDiffusionXLTextToImageUseCase
)
from yt_diffuser.types.generator.message import (
    GenerateMessage,
    GeneratorCommand
)

class GeneratorDispatchUseCase:
    """
    パイプラインに対して適切なユースケースをディスパッチする
    """

    @inject
    def __init__(
        self,
        path:AppPath,
        pipeline_store:IPipelineStore,
        pipeline_util:PipelineUtilUseCase,
        store:IGeneratorStatusStore
    ) -> None:
        """
        コンストラクタ

        Args:
            path (AppPath): アプリケーションパス
            pipeline_store (IPipelineStore): パイプラインストア
        """
        self.path = path
        self.pipeline_store = pipeline_store
        self.pipeline_util = pipeline_util
        self.store = store

    def dispatch(self, task:GenerateMessage, result_queue:Queue):
        """
        現在ストックされているパイプラインに対応するユースケースを取得し、実行する

        Args:
            generate_type (GenerateType): 生成タイプ
        """
        pipeline = self.pipeline_store.get_pipeline()

        usecase = None
        if isinstance(pipeline, StableDiffusionXLPipeline):
            if task.command == GeneratorCommand.TEXT_TO_IMAGE:

                usecase = StableDiffusionXLTextToImageUseCase(self.path, pipeline, self.pipeline_util, self.store)
                usecase.forward(task, result_queue)
        
        return
