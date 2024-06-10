from typing import Dict

from diffusers import DiffusionPipeline
from injector import inject

from yt_diffuser.types.error import ErrorMessageSignal
from yt_diffuser.types.path import AppPath
from yt_diffuser.stores.thread.interface import IThreadStore, ThreadKeys
from yt_diffuser.usecases.generator.pipeline.interface import IPipelineUseCase

class GeneratorExecuteUseCase:
    """
    パイプラインを実行するユースケース
    """

    @inject
    def __init__(self, path:AppPath, thread:IThreadStore):
        """
        コンストラクタ

        Args:
            path (AppPath): パス設定
            thread (IThreadStore): スレッドストア
        """
        self.path = path
        self.thread = thread

    def forward(self, usecase:IPipelineUseCase, pipeline:DiffusionPipeline, data:Dict) -> None:
        """
        パイプラインを実行する。

        Args:
            usecase (IPipelineUseCase): パイプラインを実行するユースケース
            pipeline (DiffusionPipeline): パイプライン
            data (dict): データ
        """
        if self.thread.is_alive(ThreadKeys.GENERATOR) == True:
            raise ErrorMessageSignal("Thread is running.")

        thread = self.thread.create_thread(ThreadKeys.GENERATOR, usecase.forward, args=(data,))
        thread.start()
    