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
    
    def load(self, base_model_name:str, base_revision:str, compile:bool) -> None:
        """
        モデルを読み込む
        
        Args:
            base_model_name (str): モデル名
            base_revision (str): リビジョン
            compile (bool): コンパイルするかどうか
        """
        self.process.run(ProcessKey.GENERATOR)
        send_queue = self.process.get_send_queue(ProcessKey.GENERATOR)

        message = GeneratorMessage(
            message_type=GeneratorMessageType.LOAD,
            data=GeneratorLoadData(
                baes_model_name=base_model_name,
                base_revision=base_revision,
                compile=compile
            ).model_dump())

        logger.debug(f"Load model: {message.data}")
        send_queue.put(message.model_dump())
