"""
route.pyのテスト
"""
import pytest

from fastapi import FastAPI

from yt_diffuser.adapters.web.route import *

def test_setup_routes():
    """
    ルーティング設定のテスト
    """
    app = FastAPI()
    setup_routes(app)
    assert True, "エラーが出なければOK"
