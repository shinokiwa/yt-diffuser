""" base.py のテスト
"""
import pytest
from pytest_mock import MockerFixture

from yt_diffuser.api.web.events.base import *

class TestEventBase:
    """
    EventBase
    """

    def test_get_listeners_spec(self, mocker: MockerFixture):
        """
        get_listeners

        it:
            - リスナーリストを取得する。
            - イベント名が未登録の場合はリストを作成する。
        """
        _listeners = mocker.patch.dict("yt_diffuser.api.web.event.base.EventBase._listeners", {})
        r = EventBase.get_listeners()
        assert type(r) == list, "リスナーリストが返却される。"
        assert "EventBase" in _listeners, "イベント名が未登録の場合はリストを作成する。"

    def test_get_event_listener_spec(self, mocker: MockerFixture):
        """
        get_event_listener

        it:
            - イベントのリスナーキューを作成し、取得する。
            - 未登録のイベント名の場合はイベントを作成する。
        """
        _listeners = mocker.patch.dict("yt_diffuser.api.web.event.base.EventBase._listeners", {})
        q = EventBase.get_event_listener()
        assert type(q) == asyncio.Queue, "リスナーキューオブジェクトが返却される。"
        assert q in _listeners["EventBase"], "リスナーキューはリストに追加される。"

    def test_remove_event_listener_spec(self, mocker: MockerFixture):
        """
        remove_event_listener

        it:
            - リスナーキューを削除する。
            - 未登録のイベント名、リスナーキューの場合は何もしない。
        """

        _listeners = mocker.patch.dict("yt_diffuser.api.web.event.base.EventBase._listeners", {})

        q1 = asyncio.Queue()
        q2 = asyncio.Queue()
        q3 = asyncio.Queue()
        _listeners["EventBase"] = [q1, q2]
        EventBase.remove_event_listener(q1)
        assert len(_listeners["EventBase"]) == 1, "実在するリスナーキューなら削除される。"
        assert _listeners["EventBase"][0] == q2, "指定したリスナーキュー以外は削除されない。"

        EventBase.remove_event_listener(q3)
        EventBase.remove_event_listener(q2)
        assert "EventBase" not in _listeners, "リスナーキューがなくなるとイベント名も削除される。"

        q = asyncio.Queue()
        EventBase.remove_event_listener(q)
        assert len(_listeners) == 0, "存在しないリスナーやイベント名は何もしない。"

    def test_send_event_spec(self, mocker: MockerFixture):
        """
        send_event

        it:
            - イベントリスナーにイベントを配信する。
        """
        _listeners = mocker.patch.dict("yt_diffuser.api.web.event.base.EventBase._listeners", {})

        q1 = asyncio.Queue()
        q2 = asyncio.Queue()
        _listeners["EventBase"] = [q1, q2]
        EventBase.send_event(data={"test": "data"})
        r1 = q1.get_nowait()
        r2 = q2.get_nowait()
        assert r1 == {"test": "data"}
        assert r2 == {"test": "data"}

        # イベント名が異なるリスナーには配信されない
        _listeners["EventBase"] = []
        _listeners['test2'] = [q1, q2]

        EventBase.send_event(data={"test2": "data2"})
        with pytest.raises(asyncio.queues.QueueEmpty):
            q1.get_nowait()
        with pytest.raises(asyncio.queues.QueueEmpty):
            q2.get_nowait()


    def test_trigger_spec(self, mocker: MockerFixture):
        """
        trigger

        it:
            - イベントをトリガーする。
        """
        send_event = mocker.patch("yt_diffuser.api.web.event.base.EventBase.send_event")
        EventBase.trigger(data={"test": "data"})

        assert send_event.called, "send_event が呼ばれる。"
        assert send_event.call_args.kwargs["data"] == {"test": "data"}, "引数がそのまま渡される。"

