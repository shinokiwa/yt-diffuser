""" route.pyのテスト
"""
import pytest
from flask import Flask

from yt_diffuser.web.route import init_routes

@pytest.mark.describe('init_routes')
@pytest.mark.it('ルーティングを設定する。')
def test_init_routes ():
    # 実際のルーティングはインテグレーションテストで確認する。
    # ここではエラーが出なければOK。
    init_routes(Flask(__name__))