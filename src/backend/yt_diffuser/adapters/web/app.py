import os
from logging import getLogger, StreamHandler, DEBUG

from fastapi import FastAPI

from yt_diffuser.injector import get_container
from .route import setup_routes
from .lifespan import LifeSpan

def create_app() -> FastAPI:
    """
    アプリケーションを作成する
    """
    if os.environ.get('DEBUG') == '1':
        logger = getLogger('yt_diffuser')
        logger.addHandler(StreamHandler())
        logger.setLevel(level=DEBUG)
    
    lifespan:LifeSpan = get_container().get(LifeSpan)

    app = FastAPI(
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        title="ゆとりでふーざーAPI",
        openapi_url="/api/openapi.json",
        version="0.0.4",
        lifespan=lifespan.execute
        )
    
    setup_routes(app)

    return app

    
