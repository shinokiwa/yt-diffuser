"""
モデル関係のenum
"""
from enum import Enum

class ModelClass (Enum):
    """
    モデル処理クラス名
    要するにベースモデルかLoRAモデルかControlNetモデルか。
    """

    BASE_MODEL = "base-model"
    LORA_MODEL = "lora-model"

    LAST_USED_MODEL = "last-used-model"

class ModelSource (Enum):
    """
    モデルソース
    要するにHuggingFace Hubか、ローカルファイルか。
    """

    HUB = "hub"
    LOCAL = "local"

class PrecisionName (Enum):
    """
    モデル精度
    """

    DEFAULT = "default"
    FP16 = "fp16"


class PipelineName (Enum):
    """
    パイプライン名
    """

    SD = "sd"
    SDXL = "sdxl"