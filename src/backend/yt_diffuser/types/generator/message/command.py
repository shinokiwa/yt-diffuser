from enum import Enum

class GeneratorCommand(Enum):
    """
    生成プロセスへのコマンド
    """
    LOAD = 'load'
    STOP = 'stop'
    EXIT = 'exit'
    TEXT_TO_IMAGE = 'text_to_image'
    IMAGE_TO_IMAGE = 'image_to_image'
    IN_PAINT = 'in_paint'
