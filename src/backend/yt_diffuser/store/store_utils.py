"""
ストア用のユーティリティ関数
"""
from typing import List
from sqlite3 import Connection

from huggingface_hub import scan_cache_dir

from yt_diffuser.config import AppConfig
from yt_diffuser.store import (
    ModelStore,
    HFModelStore
)

def model_store_factory (config: AppConfig, model_name: str, revision: str, class_name: int) -> ModelStore:
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
    if class_name == 'ModelStore':
        return ModelStore(config, model_name, revision)
    elif class_name == 'HFModelStore':
        return HFModelStore(config, model_name, revision)
    else:
        raise ValueError(f"invalid class_name: {class_name}")


def scan_model_dir(config:AppConfig, conn:Connection) -> List[ModelStore]:
    """
    ディレクトリをスキャンし、モデルストアのリストを取得する。

    Args:
        config (AppConfig): アプリケーション設定
        conn (Connection): DBコネクション

    """

    model_list = []

    if config.STORE_HF_MODEL_DIR.exists() is False:
        config.STORE_HF_MODEL_DIR.mkdir(parents=True)

    # HuggingFaceキャッシュディレクトリをスキャン
    hf_cache = scan_cache_dir(config.STORE_HF_MODEL_DIR)
    for hf_repo in hf_cache.repos:

        for hf_revision in hf_repo.revisions:

            if hf_revision.refs is None or len(hf_revision.refs) == 0:
                model_list.append(HFModelStore(config,
                    model_name=hf_repo.repo_id,
                    revision=hf_revision.commit_hash,
                    commit_hash=hf_revision.commit_hash
                ))
            else:
                model_list += [
                    HFModelStore(config,
                        model_name=hf_repo.repo_id,
                        revision=ref,
                        commit_hash=hf_revision.commit_hash,
                        ref=ref
                    ) for ref in hf_revision.refs
                ]

    return model_list