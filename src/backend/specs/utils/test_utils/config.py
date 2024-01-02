"""
テスト用ユーティリティ

AppConfig関係。
"""
import pytest
import tempfile
from pathlib import Path

from yt_diffuser.config import AppConfig

def make_config(is_memory_db:bool = False) -> AppConfig:
    """
    テスト用のアプリケーション設定を生成する。

    Args:
        is_memory_db (bool): メモリDBを使用するかどうか。
    """
    config = AppConfig(
        debug=True,
        BASE_DIR=tempfile.mkdtemp(),
        offilne=True
    )

    config.STORE_HF_MODEL_DIR = Path(__file__).parents[1] / "test_data/basic/models/huggingface"

    if is_memory_db:
        config.DB_FILE = ':memory:'

    return config