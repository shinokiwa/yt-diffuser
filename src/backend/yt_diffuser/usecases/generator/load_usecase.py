from typing import Dict
import logging; logger = logging.getLogger(__name__)

import torch
from diffusers import DiffusionPipeline
from injector import inject

from yt_diffuser.types.path import AppPath
from yt_diffuser.types.error import ErrorMessageSignal
from yt_diffuser.types.generator import GeneratorLoadData

from yt_diffuser.stores.thread.interface import IThreadStore, ThreadKeys
from yt_diffuser.stores.pipeline.interface import IPipelineStore


class GeneratorLoadUseCase:
    """
    パイプラインを読み込むユースケース
    """

    @inject
    def __init__(self, path:AppPath, pipeline:IPipelineStore, thread:IThreadStore):
        """
        コンストラクタ

        Args:
            path (AppPath): パス設定
            pipeline (IPipelineStore): パイプラインストア
            thread (IThreadStore): スレッドストア
        """
        self.path = path
        self.pipeline = pipeline
        self.thread = thread

    def load(self, input_data:Dict) -> None:
        """
        モデルを読み込む
        """
        if self.thread.is_alive(ThreadKeys.GENERATOR):
            raise ErrorMessageSignal("Generator is already running")
        
        data = GeneratorLoadData(**input_data)

        self.pipeline.clear_pipeline()
        thread = self.thread.create_thread(ThreadKeys.GENERATOR, self.thread_load, args=(data,))
        logger.debug("Load thread start.")
        thread.start()
    
    def thread_load(self, data:GeneratorLoadData) -> None:
        """
        loadの処理実体

        Args:
            data (GenerateLoadLoadMessage): ロードデータ
        """
        logger.debug("Load start.")

        pipeline = DiffusionPipeline.from_pretrained(
            pretrained_model_name_or_path=data.base_model_id,
            revision=data.base_revision,
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
        logger.debug("Load complete.")
        return