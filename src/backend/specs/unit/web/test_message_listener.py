""" message_listener.py のテスト
"""
import pytest
from unittest.mock import patch

import queue

from yt_diffuser.web.message_listener import (
    get_event_listener,
    remove_event_listener,
    get_message_queue,
    message_listener,
    start_message_listener
)

@pytest.mark.describe("get_event_listener")
@pytest.mark.it("指定したイベントのリスナーキューを取得する。リスナーキューは初期状態で最新のメッセージが入っている。")
def test_get_event_listener_spec():

    with patch("yt_diffuser.web.message_listener._listeners", {"test": []}) as _listeners, \
        patch("yt_diffuser.web.message_listener._latest_messages", {"test": "data"}) as _latest_messages:

        q = get_event_listener("test")

        assert type(q) == queue.Queue
        assert _listeners["test"][0] == q
        assert q.get_nowait() == "data"

@pytest.mark.it("イベントが存在しない場合は新規に作成する。また、最新のメッセージが存在しない場合はキューには何も入っていない。")
def test_get_event_listener_no_event():
    
        with patch("yt_diffuser.web.message_listener._listeners", {}) as _listeners, \
            patch("yt_diffuser.web.message_listener._latest_messages", {}) as _latest_messages:
    
            q = get_event_listener("test")
            assert type(q) == queue.Queue
            assert _listeners["test"][0] == q
            assert q.empty() == True


@pytest.mark.describe("remove_event_listener")
@pytest.mark.it("リスナーキューを削除する。")
def test_remove_event_listener_spec():

    with patch("yt_diffuser.web.message_listener._listeners", {"test": []}) as _listeners:
        q = queue.Queue()
        _listeners["test"].append(q)
        remove_event_listener("test", q)
        assert len(_listeners["test"]) == 0

@pytest.mark.it("イベント、リスナーキューが存在しない場合は何もしない。")
def test_remove_event_listener_no_event():

    with patch("yt_diffuser.web.message_listener._listeners", {"test": []}) as _listeners:
        q = queue.Queue()
        remove_event_listener("test", q)
        assert len(_listeners["test"]) == 0

    with patch("yt_diffuser.web.message_listener._listeners", {}) as _listeners:
        q = queue.Queue()
        remove_event_listener("test", q)
        assert len(_listeners) == 0

@pytest.mark.describe("message_listener")
@pytest.mark.it("無限ループでイベントリスナーにメッセージを転送する。exitイベントが来たら終了する。")
def test_message_listener_spec():

    with patch("yt_diffuser.web.message_listener._listeners", {}) as _listeners, \
        patch("yt_diffuser.web.message_listener._latest_messages", {}) as _latest_messages, \
        patch("yt_diffuser.web.message_listener._NO_CACHE_EVENT", ["test2"]) as _NO_CACHE_EVENT:

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


@pytest.mark.describe("start_listener")
@pytest.mark.it("リスナーを起動する。")
def test_start_listener_spec(mocker):

    mock_thread = mocker.patch("yt_diffuser.web.message_listener.threading.Thread")
    mock_message_listener = mocker.patch("yt_diffuser.web.message_listener.message_listener")

    start_message_listener()

    assert mock_thread.call_count == 1
    assert mock_thread.call_args_list[0][1]["target"] == mock_message_listener

