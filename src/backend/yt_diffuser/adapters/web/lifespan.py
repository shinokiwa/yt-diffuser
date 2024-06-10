"""
スタートアップ時に実行される処理を記述するモジュール
"""
from contextlib import asynccontextmanager
from logging import getLogger; logger = getLogger(__name__)

from fastapi import FastAPI
from injector import Injector

from yt_diffuser.injector import get_container
from yt_diffuser.usecases.web.startup_usecase import StartUpUseCase

@asynccontextmanager
async def lifespan(app: FastAPI, container:Injector = get_container()):
    """
    スタートアップ処理

    Args:
        app (FastAPI): FastAPIアプリケーション いまのところ何も関係なし
    """
    startup:StartUpUseCase = container.get(StartUpUseCase)
    startup.startup()

    try:
        yield
    finally:
        pass
