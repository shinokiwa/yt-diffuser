"""
HuggingFaceモデルのユーティリティ関数
"""
from typing import List
from sqlite3 import Connection

from huggingface_hub import scan_cache_dir

from yt_diffuser.config import AppConfig
from yt_diffuser.store.model import ModelInfo, ModelClass, ModelSource


def scan_model_dir(config:AppConfig, conn:Connection) -> List[ModelInfo]:
    """
    ディレクトリをスキャンし、モデルストアのリストを取得する。

    Args:
        config (AppConfig): アプリケーション設定
        conn (Connection): DBコネクション

    """

    model_list = []

    config.STORE_HF_MODEL_DIR.mkdir(parents=True, exist_ok=True)

    # HuggingFaceキャッシュディレクトリをスキャン
    hf_cache = scan_cache_dir(config.STORE_HF_MODEL_DIR)
    for hf_repo in hf_cache.repos:
        model = ModelInfo(
            model_name=hf_repo.repo_id,
            model_class=ModelClass.BASE_MODEL,
            source=ModelSource.HUB,
        )

        for hf_revision in hf_repo.revisions:
            if hf_revision.refs is None or len(hf_revision.refs) == 0:
                model.add_revision(hf_revision.commit_hash)
            else:
                for ref in hf_revision.refs:
                    model.add_revision(ref)
        
        model_list.append(model)

    return model_list