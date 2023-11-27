""" /api/worker/download の機能テスト
"""
import pytest
import requests

from specs.feature.testutils.app import setup_app


@pytest.mark.describe('API /api/worker/download の機能テスト')
@pytest.mark.it('ダウンロード処理を開始する。')
@pytest.mark.it('ダウンロード中はSSEで進捗を通知する。')
def test_download(setup_app):
    res = requests.post('http://localhost:8000/api/worker/download')
    assert res.status_code == 200
    assert res.json() == {'status': 'ok'}

    res = requests.get('http://localhost:8000/api/sse/progress', stream=True)

    for line in res.iter_lines():
        if line:
            print(line.decode('utf-8'))
            assert line.decode('utf-8') == 'data: {"status": "progress"}'
