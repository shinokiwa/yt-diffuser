""" main.pyのテスト
"""
import pytest
from multiprocessing import Queue
from flask import Flask

from yt_diffuser.web.main import web_procedure

@pytest.mark.describe('web_procedure')
@pytest.mark.it('it: waitressのWSGIサーバーが起動する。その際にappにAPIが登録される。')
def test_web_procedure_spec(mocker):

    app = Flask(__name__)

    mock_create_app = mocker.patch('yt_diffuser.web.main.create_app', return_value=app)
    mock_start_listener = mocker.patch('yt_diffuser.web.main.start_listener')
    mock_set_send_queue = mocker.patch('yt_diffuser.web.main.set_send_queue')
    mock_serve = mocker.patch('yt_diffuser.web.main.serve')

    sq = Queue()
    rq = Queue()
    web_procedure(send_queue=sq, recv_queue=rq)

    assert mock_create_app.call_count == 1

    assert mock_start_listener.call_count == 1
    assert mock_start_listener.call_args[0][0] == rq

    assert mock_set_send_queue.call_count == 1
    assert mock_set_send_queue.call_args[0][0] == sq

    assert mock_serve.call_count == 1
    assert mock_serve.call_args[0][0] == app
    assert mock_serve.call_args[1]["host"] == '0.0.0.0'
    assert mock_serve.call_args[1]["port"] == 8000

@pytest.mark.it('it: 環境変数DEBUGが1の場合はapp.debugがTrueになる。')
def test_web_procedure_debug(mocker):
    """ it: 環境変数DEBUGが1の場合はapp.debugがTrueになる。
    """
    mocker.patch.dict('os.environ', {'DEBUG': '1'})
    app = Flask(__name__)

    mocker.patch('yt_diffuser.web.main.create_app', return_value=app)
    mocker.patch('yt_diffuser.web.main.start_listener')
    mocker.patch('yt_diffuser.web.main.set_send_queue')
    mock_serve = mocker.patch('yt_diffuser.web.main.serve')

    sq = Queue()
    rq = Queue()
    web_procedure(send_queue=sq, recv_queue=rq)

    assert mock_serve.call_args[0][0].debug == True
