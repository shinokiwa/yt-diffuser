""" テスト用ユーティリティ
"""
import pytest
import requests
import time
import tempfile

from yt_diffuser.config import AppConfig
from yt_diffuser.web.app import create_app

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

    _app = create_app(config)
    
    return _app