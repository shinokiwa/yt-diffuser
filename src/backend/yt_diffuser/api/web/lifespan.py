"""
スタートアップ時に実行される処理を記述するモジュール
"""
from contextlib import asynccontextmanager

from logging import getLogger; logger = getLogger(__name__)

from fastapi import FastAPI, Depends

from ..usecases.startup import startup

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    スタートアップ処理
    """
    startup()
    try:
        yield
    finally:
        pass
