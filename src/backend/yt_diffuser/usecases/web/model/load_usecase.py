import logging; logger = logging.getLogger(__name__)

from injector import inject

from yt_diffuser.usecases.process import ProcessUseCase, ProcessKey
from yt_diffuser.types.generator import (
    GeneratorMessage,
    GeneratorMessageType,
    GeneratorLoadData
)

class ModelLoadUseCase:
    """
    生成プロセスの管理系処理を行うユースケース
    """

    @inject
    def __init__(
        self,
        process:ProcessUseCase
    ):
        """
        コンストラクタ
        
        Args:
            queue_store (IProcessQueueStore): キューストア
        """
        self.process = process
    
    def load(self, base_model_id:str, base_revision:str, compile:bool) -> None:
        """
        モデルを読み込む
        
        Args:
            base_model_id (str): モデル名
            base_revision (str): リビジョン
            compile (bool): コンパイルするかどうか
        """
        self.process.run(ProcessKey.GENERATOR)
        send_queue = self.process.get_send_queue(ProcessKey.GENERATOR)

        message = GeneratorMessage(
            message_type=GeneratorMessageType.LOAD,
            data=GeneratorLoadData(
                base_model_id=base_model_id,
                base_revision=base_revision,
                compile=compile
            ).model_dump())

        logger.debug(f"Load model: {message.data}")
        send_queue.put(message.model_dump())
    
    def exit(self) -> None:
        """
        生成プロセスを終了する
        """
        if self.process.is_running(ProcessKey.GENERATOR) is False:
            return

        send_queue = self.process.get_send_queue(ProcessKey.GENERATOR)
        if send_queue is None:
            return

        message = GeneratorMessage(
            message_type=GeneratorMessageType.EXIT,
            data={}
        )

        logger.debug(f"Load model: {message.data}")
        send_queue.put(message.model_dump())

