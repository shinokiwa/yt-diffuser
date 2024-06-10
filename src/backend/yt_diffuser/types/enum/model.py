"""
モデルの列挙型を定義するモジュール
"""

from enum import Enum

class ModelType(Enum):
    """
    モデルのクラスを列挙する列挙型
    """
    BASE_MODEL = 'base-model'
    LORA_MODEL = 'lora-model'
    CONTROLNET_MODEL = 'controlnet-model'

class ModelSource(Enum):
    """
    モデルの取得元を列挙する列挙型
    """
    HF = 'huggingFace'
    LOCAL = 'local'

class PipelineClass(Enum):
    """
    パイプラインのクラスを列挙する列挙型
    """
    STABLE_DIFFUSION_XL = 'StableDiffusionXL'
