from fastapi import FastAPI

from .route import setup_routes
from .lifespan import lifespan

def create_app() -> FastAPI:
    """
    アプリケーションを作成する
    """
    app = FastAPI(
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        title="ゆとりでふーざーAPI",
        openapi_url="/api/openapi.json",
        version="0.0.4",
        lifespan=lifespan
        )
    
    setup_routes(app)

    return app

    
