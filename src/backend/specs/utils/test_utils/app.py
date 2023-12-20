""" テスト用ユーティリティ
"""
import pytest
import tempfile
from pathlib import Path

from yt_diffuser.config import AppConfig
from yt_diffuser.web.app import create_app
from yt_diffuser.web.message_listener import stop_message_listener

@pytest.fixture(scope='module')
def app() -> AppConfig:
    """
    テスト用のアプリケーションをセットアップする。
    """
    config = AppConfig(
        debug=True,
        BASE_DIR=tempfile.mkdtemp(),
        offilne=True
    )

    config.STORE_HF_MODEL_DIR = Path(__file__).parents[1] / "test_models"

    _app = create_app(config)
    
    yield _app

    stop_message_listener()