"""
yt_diffuser.utils.event.process のテスト
"""
import pytest
from pytest_mock import MockerFixture

import multiprocessing

from yt_diffuser.utils.event.process import *

def test_get_context_spec():
    """
    get_context

    it:
        - プロセスコンテキストを取得する。
    """
    assert type(get_context()) == multiprocessing.context.SpawnContext

def test_get_message_queue_spec():
    """
    get_message_queue

    it:
        - メッセージキューを取得する。
    """
    assert type(get_message_queue()) == multiprocessing.queues.Queue

def test_message_listener_spec(mocker:MockerFixture):
    """
    message_listener

    it:
        - メッセージキューからメッセージを受け取り、イベントリスナーに配信する。
        - イベントが "exit" の場合、リスナーを終了する。
    """
    mock_send_event = mocker.patch("yt_diffuser.utils.event.process.send_event")

    message_queue = get_message_queue()
    message_queue.put(("test", True, {"test": "data"}))
    message_queue.put(("test2", False, {"test2": "data2"}))
    message_queue.put(("exit", False, None))
    message_listener()

    assert mock_send_event.call_count == 2
    assert mock_send_event.call_args_list[0][0][0] == "test"
    assert mock_send_event.call_args_list[0][0][1] == True
    assert mock_send_event.call_args_list[0][0][2] == {"test": "data"}

    assert mock_send_event.call_args_list[1][0][0] == "test2"
    assert mock_send_event.call_args_list[1][0][1] == False
    assert mock_send_event.call_args_list[1][0][2] == {"test2": "data2"}


def test_start_listener_spec(mocker:MockerFixture):
    """
    start_message_listener

    it:
        - メッセージリスナーを起動する。
        - メッセージリスナーは別スレッドで起動する。
        - メッセージリスナーはプロセス終了時に自動的に終了する。
    """

    mock_thread = mocker.patch("yt_diffuser.utils.event.process.threading.Thread")
    mock_message_listener = mocker.patch("yt_diffuser.utils.event.process.message_listener")

    start_message_listener()

    assert mock_thread.call_count == 1
    assert mock_thread.call_args_list[0][1]["target"] == mock_message_listener


def test_stop_listener_spec(mocker:MockerFixture):
    """
    stop_message_listener

    it:
        - メッセージリスナーを終了する。
        - 基本的にテスト用
    """

    mock_queue = mocker.MagicMock(put_nowait=mocker.MagicMock())
    mock_message_queue = mocker.patch( "yt_diffuser.utils.event.process.get_message_queue", return_value=mock_queue)
    stop_message_listener()
    assert mock_queue.put_nowait.call_count == 1
    assert mock_queue.put_nowait.call_args_list[0][0][0] == ("exit", False, None)