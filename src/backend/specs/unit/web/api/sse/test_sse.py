""" yt_diffuser.web.api.sse.sse のテスト
"""
import pytest
from flask import Flask

from yt_diffuser.web.api.sse.sse import bp

def test_sse_spec(mocker):
    """
    sse

    it:
        dowonload ダウンロードの状態を取得する
        status プロセスの状態を取得する
        message ワーカープロセスからのメッセージを取得する
    """
    mock_event_stream = mocker.patch('yt_diffuser.web.api.sse.sse.event_stream', return_value='test_event_stream')
    app = Flask(__name__)
    app.register_blueprint(bp)

    with app.test_request_context():
        urls = ['/api/sse/download', '/api/sse/status', '/api/sse/message']

        for url in urls:
            response = app.test_client().get(url)
            assert response.status_code == 200
            assert response.content_type == 'text/event-stream; charset=utf-8'
            assert response.data == b'test_event_stream'
