"""
テスト用ユーティリティ

AppConfig関係。
"""
import pytest
import tempfile
from pathlib import Path

from yt_diffuser.config import AppConfig

def make_config() -> AppConfig:
    """
    テスト用のアプリケーション設定を生成する。
    """
    config = AppConfig(
        debug=True,
        BASE_DIR=tempfile.mkdtemp(),
        offilne=True
    )

    config.STORE_HF_MODEL_DIR = Path(__file__).parents[1] / "test_data/basic/models/huggingface"

    return config