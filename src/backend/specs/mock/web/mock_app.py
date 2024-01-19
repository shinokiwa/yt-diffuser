"""
yt_diffuser.web.app のモックというかテスト用
"""
import pytest
from typing import Generator
from flask import Flask

from specs.mock.mock_config import mock_config

from yt_diffuser.web.app import create_app
from yt_diffuser.utils.event import stop_message_listener

@pytest.fixture(scope='module')
def app() -> Generator[Flask, None, None]:
    """
    テスト用のアプリケーションをセットアップする。
    AppConfigはテスト用標準を使用する。
    """
    _app = create_app(mock_config())
    
    yield _app

    stop_message_listener()