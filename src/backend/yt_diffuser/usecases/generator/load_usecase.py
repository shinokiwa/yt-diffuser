import logging; logger = logging.getLogger(__name__)
from queue import Queue

import torch
from diffusers import DiffusionPipeline
from injector import inject

from yt_diffuser.types.path import AppPath
from yt_diffuser.stores.generator.interface import IGeneratorStatusStore
from yt_diffuser.stores.pipeline.interface import IPipelineStore

from yt_diffuser.types.error import GeneratorExitSignal

from yt_diffuser.types.generator.message import (
    GenerateMessage,
    GeneratorArgsLoad,
    GeneratorStatus,
    GenerateMessageResult
)


class GeneratorLoadUseCase:
    """
    パイプラインを読み込むユースケース
    """

    @inject
    def __init__(
        self,
        path:AppPath,
        pipeline:IPipelineStore,
        store:IGeneratorStatusStore
    ):
        """
        コンストラクタ

        Args:
            path (AppPath): パス設定
            pipeline (IPipelineStore): パイプラインストア
        """
        self.path = path
        self.pipeline = pipeline
        self.store = store

    def load(self, task:GenerateMessage, result_queue:Queue) -> None:
        """
        モデルを読み込む
        """
        args = GeneratorArgsLoad(**task.args)
        result = GenerateMessageResult(
            status=GeneratorStatus.LOADING,
            base_model_id=args.base_model_id,
        )
        result_queue.put(result)

        self.pipeline.clear_pipeline()

        pipeline = DiffusionPipeline.from_pretrained(
            pretrained_model_name_or_path=args.base_model_id,
            revision=args.base_revision,
            cache_dir=self.path.STORE_HF_MODEL_DIR,
            torch_dtype=torch.bfloat16,
            use_safetensors=True,
            local_files_only=True,
            variant="fp16",
        )

        if torch.cuda.is_available():
            pipeline = pipeline.to("cuda")

        if compile:
            #compile_current_model(pipe)
            pass

        self.pipeline.set_pipeline(pipeline)

        self.store.state.base_model_id = args.base_model_id
        result.status = GeneratorStatus.LOADED
        result_queue.put(result)

        return