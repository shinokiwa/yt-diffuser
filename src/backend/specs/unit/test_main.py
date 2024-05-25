""" 
yt_diffuser.main のテスト
"""
import pytest

from yt_diffuser.main import *
from yt_diffuser.config import AppConfig

def test_main(mocker):
    """
    main

    it:
        - waitressのWSGIサーバーが起動する。その際にappにAPIが登録される。
    """
    mock_create_app = mocker.patch('yt_diffuser.main.create_app', return_value='app')
    mock_serve = mocker.patch('yt_diffuser.main.serve')

    main(config=AppConfig())

    assert mock_create_app.call_count == 1

    assert mock_serve.call_count == 1
    assert mock_serve.call_args[0][0] == 'app'
    assert mock_serve.call_args[1]["host"] == '0.0.0.0'
    assert mock_serve.call_args[1]["port"] == 8000

def test_main_debug(mocker):
    """
    main

    it:
        - 環境変数DEBUGが1の場合、デバッグモードで起動する。
            - 実際にはAppConfigのdebugを経由している。
    """
    mock_create_app = mocker.patch('yt_diffuser.main.create_app', return_value='app')
    mock_serve = mocker.patch('yt_diffuser.main.serve')

    main(config=AppConfig(debug=True))

    assert mock_create_app.call_count == 1

    assert mock_serve.call_count == 1
