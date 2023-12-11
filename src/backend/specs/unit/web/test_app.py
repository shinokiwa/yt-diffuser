""" app.pyのテスト
"""
import pytest
from flask import Flask

from yt_diffuser.web.app import create_app
from yt_diffuser.config import AppConfig

@pytest.mark.describe('create_app')
@pytest.mark.it('Flaskのインスタンスを作成する。')
def test_create_app (mocker):
    mock_init_routes = mocker.patch('yt_diffuser.web.app.init_routes')
    mock_start_listener = mocker.patch('yt_diffuser.web.app.start_message_listener')
    mock_setup_database = mocker.patch('yt_diffuser.web.app.setup_database')
    app = create_app(AppConfig())

    assert type(app) == Flask
    assert mock_init_routes.call_count == 1

    assert mock_start_listener.call_count == 1

    assert mock_setup_database.call_count == 1

