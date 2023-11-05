""" worker_listener.py のテスト """
import pytest
from unittest.mock import patch

import multiprocessing
import queue

from yt_diffuser.web.worker_listener import (
    get_listener,
    remove_listener,
    msg_callback,
    start_listener
)

@pytest.mark.describe("get_listener")
@pytest.mark.it("指定したイベントのリスナーキューを取得する。リスナーキューは初期状態で最新のメッセージが入っている。")
def test_get_listener_spec():

    with patch("yt_diffuser.web.worker_listener._listeners", {"test": []}) as _listeners, \
        patch("yt_diffuser.web.worker_listener._latest_messages", {"test": "data"}) as _latest_messages:

        q = get_listener("test")
        assert type(q) == queue.Queue
        assert _listeners["test"][0] == q
        assert q.get_nowait() == "data"

@pytest.mark.it("イベントが存在しない場合は新規に作成する。また、最新のメッセージが存在しない場合はキューには何も入っていない。")
def test_get_listener_no_event():
    
        with patch("yt_diffuser.web.worker_listener._listeners", {}) as _listeners, \
            patch("yt_diffuser.web.worker_listener._latest_messages", {}) as _latest_messages:
    
            q = get_listener("test")
            assert type(q) == queue.Queue
            assert _listeners["test"][0] == q
            assert q.empty() == True


@pytest.mark.describe("remove_listener")
@pytest.mark.it("リスナーキューを削除する。")
def test_remove_listener_spec():

    with patch("yt_diffuser.web.worker_listener._listeners", {"test": []}) as _listeners:
        q = queue.Queue()
        _listeners["test"].append(q)
        remove_listener("test", q)
        assert len(_listeners["test"]) == 0

@pytest.mark.it("イベント、リスナーキューが存在しない場合は何もしない。")
def test_remove_listener_no_event():

    with patch("yt_diffuser.web.worker_listener._listeners", {"test": []}) as _listeners:
        q = queue.Queue()
        remove_listener("test", q)
        assert len(_listeners["test"]) == 0

    with patch("yt_diffuser.web.worker_listener._listeners", {}) as _listeners:
        q = queue.Queue()
        remove_listener("test", q)
        assert len(_listeners) == 0

@pytest.mark.describe("msg_callback")
@pytest.mark.it("メッセージ受信コールバック。")
def test_msg_callback_spec():

    with patch("yt_diffuser.web.worker_listener._listeners", {}) as _listeners:
        q = queue.Queue()
        _listeners["test"] = [q]

        msg_callback(("test", "data"))
        assert q.get_nowait() == "data"

@pytest.mark.it("イベント、リスナーキューが存在しない場合は何もしない。")
def test_msg_callback_no_event():
    
        with patch("yt_diffuser.web.worker_listener._listeners", {}) as _listeners:
            msg_callback(("test", "data"))
            assert len(_listeners) == 0
    
        with patch("yt_diffuser.web.worker_listener._listeners", {"test": []}) as _listeners:
            msg_callback(("test", "data"))
            assert len(_listeners) == 1

@pytest.mark.describe("start_listener")
@pytest.mark.it("リスナーを起動する。")
def test_start_listener_spec(mocker):

    mock_thread = mocker.patch("yt_diffuser.web.worker_listener.threading.Thread")
    mock_infinite_loop = mocker.patch("yt_diffuser.web.worker_listener.infinite_loop")

    q = multiprocessing.Queue()
    start_listener(q)

    assert mock_thread.call_count == 1
    assert mock_thread.call_args_list[0][1]["target"] == mock_infinite_loop
    assert mock_thread.call_args_list[0][1]["args"] == (q, msg_callback)

