from enum import Enum

class GenerateType(str, Enum):
    """
    生成タイプ
    """
    TEXT_TO_IMAGE = 'text_to_image'
    IMAGE_TO_IMAGE = 'image_to_image'
    IN_PAINT = 'in_paint'




