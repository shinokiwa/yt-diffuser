"""
yt_diffuser.web.api.generate.status のテスト
"""
import pytest
import queue

from flask import Flask

from specs.mock.web.mock_app import app
from yt_diffuser.web.api.generate.status import *

def test_generate_status_spec(mocker, app:Flask):
    """
    generate_status

    it:
        - 生成ワーカーのステータスを返すSSE
    """
    mock_event_stream = mocker.patch('yt_diffuser.web.api.generate.status.event_stream', return_value='test_event_stream')

    with app.test_client() as client:
        response = client.get('/api/generate/status')
        assert response.status_code == 200
        assert response.content_type == 'text/event-stream; charset=utf-8'
        assert response.data == b'test_event_stream'
        assert mock_event_stream.call_count == 1
    
def test_event_stream(mocker):
    """
    event_stream

    it:
        - メッセージリスナーからのメッセージを取得し、データを文字列として返す。
        - データはSSE向けに data: value\n\n の形式になる。
        - データは辞書型が前提。
        - SSEのタイムアウトを回避するため、5秒間データがなかった場合は空(data: \n\n)のデータを返す。
        - GeneratorExitが発生した場合、メッセージリスナーから削除する。
    """
    q = queue.Queue()
    mock_listener = mocker.patch('yt_diffuser.web.api.generate.status.get_event_listener', return_value=q)
    mock_remove_listener = mocker.patch('yt_diffuser.web.api.generate.status.remove_event_listener')

    output = event_stream(0.1)
    assert next(output) == ': keep-alive\n\n'
    assert mock_listener.call_count == 1
    assert mock_listener.call_args[0][0] == 'generator'

    q.put({'label':'test_data'})
    assert next(output) == 'data: {"label": "test_data"}\n\n'

    assert mock_remove_listener.call_count == 0
    output.close()
    assert mock_remove_listener.call_count == 1