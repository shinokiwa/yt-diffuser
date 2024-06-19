"""
lifespan.py のテスト
"""
import pytest
from pytest_mock import MockerFixture

from fastapi import FastAPI

from yt_diffuser.adapters.web.lifespan import LifeSpan

class TestLifeSpan:
    """
    LifeSpanのテスト
    """
    @pytest.mark.asyncio
    async def test_execute(self, mocker: MockerFixture):
        """
        execute

        it:
            - スタートアップ処理が呼ばれること
            - リスナーが起動すること
        """
        startup = mocker.MagicMock()
        process_event = mocker.MagicMock()
        app = FastAPI()
        lifespan = LifeSpan(startup=startup, process_event=process_event)

        async with lifespan.execute(app):
            assert startup.startup.called, "スタートアップ処理が呼ばれていること"
            assert process_event.listen.called, "リスナーが起動していること"

        assert startup.shutdown.called, "シャットダウン処理が呼ばれていること"
