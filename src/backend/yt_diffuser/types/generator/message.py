from typing import Dict
from enum import Enum

from pydantic import BaseModel

class GeneratorMessageType(str, Enum):
    """
    生成プロセスへのメッセージタイプ
    """
    LOAD = 'load'
    STOP = 'stop'
    EXIT = 'exit'
    TEXT_TO_IMAGE = 'text_to_image'
    IMAGE_TO_IMAGE = 'image_to_image'
    IN_PAINT = 'in_paint'

class GeneratorMessage(BaseModel):
    """
    生成プロセスへのメッセージ
    """
    message_type: str
    data: Dict = None



