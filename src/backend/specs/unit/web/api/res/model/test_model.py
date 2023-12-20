""" modelモジュールのテスト """

from flask import Flask

from specs.utils.test_utils.app import app
from yt_diffuser.web.api.res.model import bp

def test_get_model (app:Flask):
    """
    get_model

    it:
        保存済みのモデル一覧を取得する。
    """
    with app.test_client() as client:
        response = client.get('/api/res/model')
        data = response.get_json()

        assert data['models'] == []
