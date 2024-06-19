import logging; logger = logging.getLogger(__name__)
from typing import Dict

from injector import inject

from yt_diffuser.usecases.process import ProcessUseCase, ProcessKey
from yt_diffuser.types.generator.message import GenerateMessage, GeneratorCommand, GeneratorArgsLoad

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
    
    def load(self, input_data:Dict) -> None:
        """
        モデルを読み込む
        
        Args:
            input_data (Dict): 入力データ GenerateMessageLoadEntityに変換可能であること
        """
        self.process.run(ProcessKey.GENERATOR)
        send_queue = self.process.get_send_queue(ProcessKey.GENERATOR)

        message = GenerateMessage(
            command=GeneratorCommand.LOAD,
            args=GeneratorArgsLoad(**input_data).model_dump()
        )

        logger.debug(f"Load model: {message.args['base_model_id']}")
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

        message = GenerateMessage(
            command=GeneratorCommand.EXIT
        )

        send_queue.put(message.model_dump())

