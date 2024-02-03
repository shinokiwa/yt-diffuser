"""
ストア用のユーティリティ関数
"""
from sqlite3 import Connection

from huggingface_hub import scan_cache_dir

from yt_diffuser.config import AppConfig
from yt_diffuser.store.model import ModelInfo, ModelClass, ModelSource

from .hf_model import scan_model_dir

def get_model_list(config:AppConfig, conn:Connection) -> dict:
    """
    全てのモデルのリストを取得する。

    Args:
        config (AppConfig): アプリケーション設定
        conn (Connection): DBコネクション

    """
    model_list = []

    # HuggingFaceキャッシュディレクトリをスキャン
    hf_models = scan_model_dir(config, conn)
    for model in hf_models:
        data = model.to_dict()
        model_list.append(data)

    return model_list
    


