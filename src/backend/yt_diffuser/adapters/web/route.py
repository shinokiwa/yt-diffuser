"""
ルーティング設定
"""
from importlib import import_module

from fastapi import FastAPI

def setup_routes(app:FastAPI):
    """
    ルーティング設定
    """
    app.include_router(import_module('yt_diffuser.adapters.web.routers.generate.text_to_image').router)

    app.include_router(import_module('yt_diffuser.adapters.web.routers.form.index').router)

    app.include_router(import_module('yt_diffuser.adapters.web.routers.model.index').router)
    app.include_router(import_module('yt_diffuser.adapters.web.routers.model.load').router)

    app.include_router(import_module('yt_diffuser.adapters.web.routers.server.status').router)
    app.include_router(import_module('yt_diffuser.adapters.web.routers.server.event').router)

    app.include_router(import_module('yt_diffuser.adapters.web.routers.temp.index').router)