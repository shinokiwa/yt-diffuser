"""
server_event_usecase.py のテスト
"""
import pytest
from pytest_mock import MockerFixture

import asyncio

from yt_diffuser.usecases.web.event.server_event_usecase import (
    ServerEventUseCase,
    ServerEventType,
    ServerEventData,
    ServerEventDataGenerateProgress,
    IEventListnerStore
)

class TestServerEventUseCase:

    def test_get_listener(self, mocker: MockerFixture):
        """
        get_listener

        it:
            - イベントリスナーを取得する。
        """
        store = mocker.MagicMock(spec=IEventListnerStore)
        usecase = ServerEventUseCase(store)
        listener = usecase.get_listener()

        assert isinstance(listener, asyncio.Queue), "イベントリスナーは asyncio.Queue であること"
        assert store.add.call_args.args[0] == "server", "イベント名 server が追加されていること"
        assert store.add.call_args.args[1] == listener, "イベントリスナーが追加されていること"

    def test_trigger(self, mocker: MockerFixture):
        """
        trigger

        it:
            - イベントリスナーにイベントを配信する。
        """
        listener = asyncio.Queue()
        store = mocker.MagicMock(spec=IEventListnerStore)
        store.get.return_value=[listener]

        usecase = ServerEventUseCase(store)

        data = ServerEventData(
            type=ServerEventType.INFO,
            status="test",
            generator_progress=ServerEventDataGenerateProgress()
        )

        usecase.trigger(data)
        assert listener.get_nowait() == {
            "type": ServerEventType.INFO,
            "status": "test",
            "generator_progress": {
                "generate_total": 0,
                "generate_count": 0,
                "steps_total": 0,
                "steps_count": 0,
                "percentage": 0,
                "elapsed": 0,
                "remaining": 0,
                "average": 0
            }
        }, "イベントデータが配信されていること"
