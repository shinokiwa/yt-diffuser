""" main.pyのテスト
"""
import pytest
from flask import Flask

from yt_diffuser import __main__
from yt_diffuser.config import AppConfig

@pytest.mark.describe('web_procedure')
@pytest.mark.it('it: waitressのWSGIサーバーが起動する。その際にappにAPIが登録される。')
def test_main(mocker):

    app = Flask(__name__)

    mock_create_app = mocker.patch('yt_diffuser.__main__.create_app', return_value=app)
    mock_serve = mocker.patch('yt_diffuser.__main__.serve')

    __main__.main(
        config=AppConfig(),
        debug=False
    )

    assert mock_create_app.call_count == 1

    assert mock_serve.call_count == 1
    assert mock_serve.call_args[0][0] == app
    assert mock_serve.call_args[1]["host"] == '0.0.0.0'
    assert mock_serve.call_args[1]["port"] == 8000

@pytest.mark.it('it: 環境変数DEBUGが1の場合はapp.debugがTrueになる。')
def test_main_debug(mocker):
    """ it: 環境変数DEBUGが1の場合はapp.debugがTrueになる。
    """
    mocker.patch.dict('os.environ', {'DEBUG': '1'})
    app = Flask(__name__)

    mock_create_app = mocker.patch('yt_diffuser.__main__.create_app', return_value=app)
    mock_serve = mocker.patch('yt_diffuser.__main__.serve')

    __main__.main(
        config=AppConfig(),
        debug=True
    )

    assert mock_create_app.call_count == 1
    assert mock_create_app.call_args[1]['debug'] == True
