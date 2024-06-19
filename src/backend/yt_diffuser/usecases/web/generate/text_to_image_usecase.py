import logging; logger = logging.getLogger(__name__)
from typing import Dict

from injector import inject

from yt_diffuser.types.error import NoProcessError
from yt_diffuser.types.generator.message import GenerateMessage, GeneratorCommand, GeneratorArgsTextToImage
from yt_diffuser.usecases.process import ProcessUseCase, ProcessKey

class GenerateTextToImageUseCase:
    """
    Web側TextToImage生成処理を行うユースケース
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
    
    def text_to_image(
            self,
            input_data: Dict
        ) -> None:
        """
        TextToImage生成メッセージを送信する。
        
        Args:
            input_data (Dict): 入力データ GenerateMessageTextToImageEntityに変換可能であること
        """
        if self.process.is_running(ProcessKey.GENERATOR) is False:
            raise NoProcessError("Generator process is not running.")

        send_queue = self.process.get_send_queue(ProcessKey.GENERATOR)
        message = GenerateMessage(
            command=GeneratorCommand.TEXT_TO_IMAGE,
            args=GeneratorArgsTextToImage(**input_data).model_dump()
        )
        send_queue.put(message.model_dump())

