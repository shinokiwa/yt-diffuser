""" app.pyのテスト
"""
import pytest
from flask import Flask
from pathlib import Path
import tempfile

from yt_diffuser.web.app import create_app
from yt_diffuser.config import AppConfig

def test_create_app (mocker):
    """
    create_app

    it:
        - Flaskのインスタンスを作成する。
    """
    mock_init_routes = mocker.patch('yt_diffuser.web.app.init_routes')
    mock_start_listener = mocker.patch('yt_diffuser.web.app.start_message_listener')
    mock_setup_database = mocker.patch('yt_diffuser.web.app.setup_database')

    config = AppConfig(
        BASE_DIR=Path(tempfile.mkdtemp())
    )
    app = create_app(config)

    assert type(app) == Flask
    assert mock_init_routes.call_count == 1
    assert mock_start_listener.call_count == 1
    assert mock_setup_database.call_count == 1
    assert config.DB_FILE.parent.exists() == True

    # DB_FILEがPathでないときはディレクトリを作成しない。
    # 判断しようがないのでエラーが出なければ良い。
    config = AppConfig(
        BASE_DIR=Path(tempfile.mkdtemp()),
        DB_FILE="file:memdb1?mode=memory&cache=shared"
    )
    app = create_app(config)
