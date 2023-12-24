""" テスト用ユーティリティ
"""
import pytest

from specs.utils.test_utils.config import make_config

from yt_diffuser.config import AppConfig
from yt_diffuser.web.app import create_app
from yt_diffuser.web.message_listener import stop_message_listener

@pytest.fixture(scope='module')
def app() -> AppConfig:
    """
    テスト用のアプリケーションをセットアップする。
    """
    config = make_config()

    _app = create_app(config)
    
    yield _app

    stop_message_listener()
