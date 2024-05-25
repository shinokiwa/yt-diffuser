"""
yt_diffuser.utils.message_queue のテスト
"""
import pytest
from multiprocessing import Queue

from yt_diffuser.utils.message_queue import *

@pytest.fixture
def queue (mocker):
    mock_queue = mocker.patch('yt_diffuser.utils.message_queue.Queue')
    mock_queue.put = mocker.MagicMock()
    return mock_queue

def test_send_message (queue):
    """
    send_message

    it:
        - メッセージイベントを送信する。
    """
    send_generate_status(queue, 'test', a=1, b=2)

    assert queue.put.call_count == 1
    (event, data) = queue.put.call_args[0][0]
    assert event == EVENT_TYPE_MESSAGE
    assert data['label'] == 'test'
    assert data['a'] == 1
    assert data['b'] == 2


def test_send_ready (queue):
    """
    send_ready

    it:
        - 準備完了イベントを送信する。
    """
    send_ready(queue, 'test', 'target')

    assert queue.put.call_count == 1
    (event, data) = queue.put.call_args[0][0]
    assert event == 'test'
    assert data['target'] == 'target'
    assert data['status'] == 'ready'

def test_send_progress (queue):
    """
    send_progress

    it:
        - 進捗イベントを送信する。
    """
    send_progress(queue, 'test', 'target', 100, 10, 10.0, 10.0, 10.0)

    assert queue.put.call_count == 1
    (event, data) = queue.put.call_args[0][0]
    assert event == 'test'
    assert data['target'] == 'target'
    assert data['status'] == 'progress'
    assert data['total'] == 100
    assert data['progress'] == 10
    assert data['percentage'] == 10.0
    assert data['elapsed'] == 10.0
    assert data['remaining'] == 10.0


def test_send_filesystem (queue):
    """
    send_filesystem

    it:
        - ファイルシステムイベントを送信する。
    """
    send_filesystem(queue, 'test_type', 'test_target')

    assert queue.put.call_count == 1
    (event, data) = queue.put.call_args[0][0]
    assert event == EVENT_TYPE_FILESYSTEM
    assert data['type'] == 'test_type'
    assert data['target'] == 'test_target'