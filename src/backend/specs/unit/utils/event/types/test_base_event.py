"""
yt_diffuser.utils.event.types のテスト
"""
import pytest
from pytest_mock import MockerFixture

import multiprocessing

from yt_diffuser.utils.event import Empty
from yt_diffuser.utils.event.types.base_event import *

class TestBaseEvent:

    def test_get_listener_spec(self, mocker:MockerFixture):
        """
        get_listener
        remove_listener
        send

        it:
            - イベントリスナーを取得する。
            - イベントリスナーを削除する。
            - イベントを送信する。
        """
        class TestEvent (BaseEvent):
            event_name = "test"
        
        mock_get_event_listener     = mocker.patch("yt_diffuser.utils.event.types.base_event.get_event_listener", return_value="test_queue")
        mock_remove_event_listener  = mocker.patch("yt_diffuser.utils.event.types.base_event.remove_event_listener")
        mock_send_event             = mocker.patch("yt_diffuser.utils.event.types.base_event.send_event")

        q = TestEvent.get_listener()
        assert q == "test_queue"
        assert mock_get_event_listener.call_args.args[0] == "test"
        assert mock_get_event_listener.call_count == 1

        TestEvent.send({"test": "data"})
        assert mock_send_event.call_args.args[0] == "test"
        assert mock_send_event.call_args.args[1] == True
        assert mock_send_event.call_args.args[2] == {"test": "data"}

        TestEvent.remove_listener(q)
        assert mock_remove_event_listener.call_args.args[0] == "test"
        assert mock_remove_event_listener.call_args.args[1] == q

    def test_send_process_spec(self, mocker:MockerFixture):
        """
        send_process

        it:
            - 別プロセスにイベントを送信する。
        """
        class TestEvent (BaseEvent):
            event_name = "test"
        
        q = multiprocessing.Queue()

        TestEvent.send_process(q, {"test": "data"})
        assert q.get() == ("test", True, {"test": "data"})