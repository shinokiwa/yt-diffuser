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

class ModelSource (Enum):
    """
    モデルソース
    要するにHuggingFace Hubか、ローカルファイルか。
    """

    HUB = "hub"
    LOCAL = "local"
