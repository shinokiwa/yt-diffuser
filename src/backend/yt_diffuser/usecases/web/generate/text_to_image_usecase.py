import logging; logger = logging.getLogger(__name__)

from injector import inject

from yt_diffuser.types.generator import (
    GeneratorMessage,
    GeneratorMessageType,
    GeneratorTextToImageMessage,
)
from yt_diffuser.types.error import NoProcessError
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
            prompt:str,
        ) -> None:
        """
        TextToImage生成メッセージを送信する。
        
        Args:
            model_name (str): モデル名
            revision (str): リビジョン
            compile (bool): コンパイルするかどうか
        """
        if self.process.is_running(ProcessKey.GENERATOR) is False:
            raise NoProcessError("Generator process is not running.")

        send_queue = self.process.get_send_queue(ProcessKey.GENERATOR)

        message = GeneratorMessage(
            message_type=GeneratorMessageType.TEXT_TO_IMAGE,
            data=GeneratorTextToImageMessage(
                prompt=prompt
            ).model_dump())

        send_queue.put(message.model_dump())

