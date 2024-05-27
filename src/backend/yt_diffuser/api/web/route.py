"""
ルーティング設定
"""
from importlib import import_module

from fastapi import FastAPI

def setup_routes(app:FastAPI):
    """
    ルーティング設定
    """
    app.include_router(import_module('yt_diffuser.api.web.routers.server.status').router)
    app.include_router(import_module('yt_diffuser.api.web.routers.server.event').router)