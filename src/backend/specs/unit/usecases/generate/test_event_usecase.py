"""
server_event_usecase.py のテスト
"""
import pytest
from pytest_mock import MockerFixture

import asyncio

from yt_diffuser.usecases.web.event.event_usecase import (
    EventUseCase,
    IEventListnerStore,
    WebEventEntity,
    WebEventType
)

class TestGenerateEventUseCase:

    def test_get_listener(self, mocker: MockerFixture):
        """
        get_listener

        it:
            - イベントリスナーを取得する。
        """
        store = mocker.MagicMock(spec=IEventListnerStore)
        usecase = EventUseCase(store)
        listener = usecase.get_listener(WebEventType.GENERATOR)

        assert isinstance(listener, asyncio.Queue), "イベントリスナーは asyncio.Queue であること"
        assert store.add.call_args.args[0] == WebEventType.GENERATOR.value, "イベントリスナーが追加されていること"
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

        usecase = EventUseCase(store)

        event = WebEventEntity(
            type=WebEventType.GENERATOR
        )

        usecase.trigger(event.model_dump())
        result = listener.get_nowait()
        assert result["type"] == WebEventType.GENERATOR, "イベントデータが配信されていること"
        