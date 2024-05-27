"""
server.py のテスト
"""
import pytest
from pytest_mock import MockerFixture

from yt_diffuser.api.web.events.server import *

class TestServerEvent:
    """
    ServerEvent
    """

    def test_trigger_spec(self, mocker: MockerFixture):
        """
        trigger

        it:
            - イベントをトリガーする。
        """
        send_event = mocker.patch("yt_diffuser.api.web.event.base.EventBase.send_event")

        data = ServerEventData(type=ServerEventType.INFO, status="test")
        ServerEvent.trigger(data)

        assert send_event.call_count == 1, "send_event が呼ばれる。"
        assert send_event.call_args[1]["data"] == data.model_dump(), "引数はServerEventDataのmodel_dump()。"