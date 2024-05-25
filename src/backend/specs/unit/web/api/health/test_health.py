""" yt_diffuser.web.api.health モジュールのテスト
"""
import pytest
from flask import Flask

from yt_diffuser.web.api.health import bp

@pytest.mark.describe('/api/health')
@pytest.mark.it('ヘルスチェックとして、"ok"を返す')
def test_health():
    app = Flask(__name__)
    app.register_blueprint(bp)

    with app.test_client() as client:
        response = client.get('/api/health')
        assert response.status_code == 200
        assert response.text == 'ok'
    