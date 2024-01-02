""" テスト用ユーティリティ
"""
import pytest
from typing import Generator
from flask import Flask

from specs.utils.test_utils.config import make_config

from yt_diffuser.config import AppConfig
from yt_diffuser.web.app import create_app
from yt_diffuser.web.message_listener import stop_message_listener

@pytest.fixture(scope='module')
def app() -> Generator[Flask, None, None]:
    """
    テスト用のアプリケーションをセットアップする。
    """
    config = make_config()

    _app = create_app(config)
    
    yield _app

    stop_message_listener()
