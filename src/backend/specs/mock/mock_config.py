"""
yt_diffuser.config のテスト用モックというか、テスト用設定値
"""
import pytest
import tempfile
from pathlib import Path

from yt_diffuser.config import AppConfig

def mock_config() -> AppConfig:
    """
    テスト用のアプリケーション設定を生成する。
    """
    config = AppConfig(
        debug=True,
        BASE_DIR=tempfile.mkdtemp(),
        offline=True
    )

    config.STORE_HF_MODEL_DIR = Path(__file__).parent / "data/basic/models/huggingface"
    return config