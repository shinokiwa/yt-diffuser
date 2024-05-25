""" listener.py のテスト
"""
import pytest
from pytest_mock import MockerFixture

from yt_diffuser.utils.event.listener import *

def test_get_event_listener_spec(mocker:MockerFixture):
    """
    get_event_listener

    it:
        - 指定したイベントのリスナーキューを作成し、取得する。
        - キャッシュ対象のイベントは最初に最新のキャッシュメッセージが格納される。
        - 未登録のイベント名の場合はイベントを作成する。
    """

    _listeners = mocker.patch.dict("yt_diffuser.utils.event.listener._listeners", {"test": []})
    mocker.patch.dict("yt_diffuser.utils.event.listener._latest_messages", {"test": "data"})

    q = get_event_listener("test")

    assert type(q) == queue.Queue
    assert _listeners["test"][0] == q
    assert "test2" not in _listeners
    assert q.get_nowait() == "data"

    q = get_event_listener("test2")
    assert _listeners["test2"][0] == q
    with pytest.raises(queue.Empty):
        q.get_nowait()


def test_remove_event_listener_spec(mocker:MockerFixture):
    """
    remove_event_listener

    it:
        - リスナーキューを削除する。
        - 未登録のイベント名、リスナーキューの場合は何もしない。
    """

    _listeners = mocker.patch.dict("yt_diffuser.utils.event.listener._listeners", {"test": []})
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

def test_send_event_spec(mocker:MockerFixture):
    """
    event_listener

    it:
        - イベントリスナーにメッセージを配信する。

    test:
        - データを参照渡ししていると、
          どこかのリスナーがデータを変更すると他のリスナーにも影響が出るため、
          データをコピーして配信するようにした。
    """
    _listeners = mocker.patch.dict("yt_diffuser.utils.event.listener._listeners", {"test": []})
    _latest_messages = mocker.patch.dict("yt_diffuser.utils.event.listener._latest_messages", {"test": "data"})

    q1 = queue.Queue()
    q2 = queue.Queue()
    _listeners["test"] = [q1, q2]

    send_event("test", data={"test": "data"})
    r1 = q1.get_nowait()
    r2 = q2.get_nowait()
    assert r1 == {"test": "data"}
    assert r2 == {"test": "data"}
    # コピーなので、r1とr2は別オブジェクト
    assert r1 is not r2

    assert _latest_messages["test"] == {"test": "data"}

    send_event("test2", cache=False, data={"test2": "data2"})

    with pytest.raises(queue.Empty):
        q1.get_nowait()
    with pytest.raises(queue.Empty):
        q2.get_nowait()
    
    assert "test2" not in _latest_messages
