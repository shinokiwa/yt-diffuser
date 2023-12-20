"""
ストアクラス用のユーティリティ関数
"""

from yt_diffuser.config import AppConfig
from yt_diffuser.store import (
    ModelStore,
    HFModelStore,
    MODEL_CLASS_NAME
)

def model_factory (config: AppConfig, model_name: str, revision: str, class_name: int) -> ModelStore:
    """
    モデルストアクラスのインスタンスを生成する。

    Args:
        config (AppConfig): アプリケーション設定
        model_name (str): モデル名
        revision (str): モデルのリビジョン
        class_name (int): モデルストアクラスの区分値

    Returns:
        ModelStore: モデルストアクラスのインスタンス
    """
    if class_name == MODEL_CLASS_NAME['ModelStore']:
        return ModelStore(config, model_name, revision)
    elif class_name == MODEL_CLASS_NAME['HFModelStore']:
        return HFModelStore(config, model_name, revision)
    else:
        raise ValueError(f"invalid class_name: {class_name}")