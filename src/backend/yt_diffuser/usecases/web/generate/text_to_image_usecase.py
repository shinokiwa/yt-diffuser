import logging; logger = logging.getLogger(__name__)

from injector import inject

from yt_diffuser.types.generator import (
    GeneratorMessage,
    GeneratorMessageType,
    GeneratorTextToImageData
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
            generate_count:int,
            prompt:str,
            negative_prompt:str,
            scheduler:str
        ) -> None:
        """
        TextToImage生成メッセージを送信する。
        
        Args:
        """
        if self.process.is_running(ProcessKey.GENERATOR) is False:
            raise NoProcessError("Generator process is not running.")

        send_queue = self.process.get_send_queue(ProcessKey.GENERATOR)

        message = GeneratorMessage(
            message_type=GeneratorMessageType.TEXT_TO_IMAGE,
            data=GeneratorTextToImageData(
                generate_count=generate_count,
                prompt=prompt,
                negative_prompt=negative_prompt,
                scheduler=scheduler
            ).model_dump())

        send_queue.put(message.model_dump())

