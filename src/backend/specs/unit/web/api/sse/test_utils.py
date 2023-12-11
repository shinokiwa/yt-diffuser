""" yt_diffuser.web.api.sse.utils のテスト
"""
import pytest
import queue

from yt_diffuser.web.api.sse.utils import event_stream

def test_event_stream_spec(mocker):
    """
    event_stream

    it:
        メッセージリスナーからのメッセージを取得し、データを文字列として返す
        データはSSE向けに data: value\n\n の形式になる
        データが辞書型だった場合、JSONを文字列化した形式になる
        SSEのタイムアウトを回避するため、5秒間データがなかった場合は空のデータを返す
        GeneratorExitが発生した場合、メッセージリスナーから削除する
    """
    q = queue.Queue()
    mock_listener = mocker.patch('yt_diffuser.web.api.sse.utils.get_event_listener', return_value=q)
    mock_remove_listener = mocker.patch('yt_diffuser.web.api.sse.utils.remove_event_listener')

    output = event_stream('test_event', 0.1)
    assert next(output) == 'data: \n\n'
    assert mock_listener.call_count == 1
    assert mock_listener.call_args[0][0] == 'test_event'

    q.put('test_data')
    assert next(output) == 'data: test_data\n\n'

    q.put({'test_key': 'test_value'})
    assert next(output) == 'data: {"test_key": "test_value"}\n\n'

    assert mock_remove_listener.call_count == 0
    output.close()
    assert mock_remove_listener.call_count == 1