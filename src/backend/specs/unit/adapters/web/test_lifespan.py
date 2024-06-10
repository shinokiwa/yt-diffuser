"""
lifespan.py のテスト
"""
import pytest
from pytest_mock import MockerFixture

from fastapi import FastAPI

from specs.unit.injector import get_container
from yt_diffuser.adapters.web.lifespan import lifespan, StartUpUseCase

@pytest.mark.asyncio
async def test_lifespan(mocker: MockerFixture):
    """
    lifespan

    it:
        - FastAPIアプリケーションのスタートアップ処理
    """
    app = FastAPI()
    startup = mocker.MagicMock()
    container = get_container()

    def injector ():
        return startup
    
    container.binder.bind(StartUpUseCase, to=injector)

    async with lifespan(app, container):
        assert startup.startup.called, "スタートアップユースケースが呼ばれていること"