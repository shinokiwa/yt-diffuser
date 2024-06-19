"""
スタートアップ時に実行される処理を記述するモジュール
"""
from contextlib import asynccontextmanager
from logging import getLogger; logger = getLogger(__name__)
from threading import Thread

from fastapi import FastAPI
from injector import inject

from yt_diffuser.usecases.web.startup_usecase import StartUpUseCase
from yt_diffuser.usecases.web.event.message_listener_usecase import WebMessageListenerUseCase

class LifeSpan:
    """
    スタートアップ時に実行される処理を記述するクラス
    """

    @inject
    def __init__(self, startup:StartUpUseCase, process_event:WebMessageListenerUseCase):
        self.startup = startup
        self.process_event = process_event
        
    @asynccontextmanager
    async def execute(self, app: FastAPI):
        """
        スタートアップ処理

        Args:
            app (FastAPI): FastAPIアプリケーション いまのところ何も関係なし
        """
        self.startup.startup()

        listener = Thread(target=self.process_event.listen)
        listener.start()

        try:
            yield
        finally:
            self.startup.shutdown()
