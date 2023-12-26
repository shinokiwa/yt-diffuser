""" message_listener.py のテスト
"""
import pytest
from pytest_mock import MockerFixture

import queue
import multiprocessing

from yt_diffuser.web.message_listener import *

def test_get_event_listener_spec(mocker:MockerFixture):
    """
    get_event_listener

    it:
        - 指定したイベントのリスナーキューを作成し、取得する。
        - リスナーキューは最初に最新のキャッシュメッセージが格納される。
        - 未登録のイベント名の場合はイベントを作成する。
        - ハートビートも兼ねて、最新のメッセージがない場合は空文字列が格納される。
    """

    _listeners = mocker.patch.dict("yt_diffuser.web.message_listener._listeners", {"test": []})
    mocker.patch.dict("yt_diffuser.web.message_listener._latest_messages", {"test": "data"})

    q = get_event_listener("test")

    assert type(q) == queue.Queue
    assert _listeners["test"][0] == q
    assert "test2" not in _listeners
    assert q.get_nowait() == "data"

    q = get_event_listener("test2")
    assert _listeners["test2"][0] == q
    assert q.get_nowait() == ""


def test_remove_event_listener_spec(mocker:MockerFixture):
    """
    remove_event_listener

    it:
        - リスナーキューを削除する。
        - 未登録のイベント名、リスナーキューの場合は何もしない。
    """

    _listeners = mocker.patch.dict("yt_diffuser.web.message_listener._listeners", {"test": []})
    q1 = queue.Queue()
    q2 = queue.Queue()
    q3 = queue.Queue()
    _listeners["test"].append(q1)
    _listeners["test"].append(q2)
    remove_event_listener("test", q1)
    assert len(_listeners["test"]) == 1
    assert _listeners["test"][0] == q2

    remove_event_listener("test", q3)
    assert len(_listeners["test"]) == 1

    remove_event_listener("test", q2)
    assert "test" not in _listeners

    q = queue.Queue()
    remove_event_listener("test2", q)
    assert len(_listeners) == 0

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
        - 最新のメッセージは _latest_messages に格納され、新規リスナーには最新のメッセージが配信される。
        - _NO_CACHE_EVENT に指定されたイベントは最新メッセージをキャッシュしない。
    """

    _listeners = mocker.patch.dict("yt_diffuser.web.message_listener._listeners", {"test": []})
    _latest_messages = mocker.patch.dict("yt_diffuser.web.message_listener._latest_messages", {})
    _NO_CACHE_EVENT = mocker.patch("yt_diffuser.web.message_listener._NO_CACHE_EVENT", ["test2"])

    q = queue.Queue()
    _listeners["test"] = [q]

    message_queue = get_message_queue()
    message_queue.put(("test", "data"))
    message_queue.put(("test2", "data"))
    message_queue.put(("exit", None))
    message_listener()
    assert q.get_nowait() == "data"
    assert _latest_messages["test"] == "data"
    assert "test2" not in _latest_messages


def test_start_listener_spec(mocker:MockerFixture):
    """
    start_message_listener

    it:
        - メッセージリスナーを起動する。
        - メッセージリスナーは別スレッドで起動する。
        - メッセージリスナーはプロセス終了時に自動的に終了する。
    """

    mock_thread = mocker.patch("yt_diffuser.web.message_listener.threading.Thread")
    mock_message_listener = mocker.patch("yt_diffuser.web.message_listener.message_listener")

    start_message_listener()

    assert mock_thread.call_count == 1
    assert mock_thread.call_args_list[0][1]["target"] == mock_message_listener


def test_stop_listener_spec(mocker:MockerFixture):
    """
    stop_message_listener

    it:
        - メッセージリスナーを終了する。
    """

    mock_queue = mocker.MagicMock(put_nowait=mocker.MagicMock())
    mock_message_queue = mocker.patch( "yt_diffuser.web.message_listener.get_message_queue", return_value=mock_queue)
    stop_message_listener()
    assert mock_queue.put_nowait.call_count == 1
    assert mock_queue.put_nowait.call_args_list[0][0][0] == ("exit", None)