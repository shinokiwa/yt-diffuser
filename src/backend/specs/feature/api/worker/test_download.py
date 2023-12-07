""" /api/worker/download の機能テスト
"""
import pytest
import requests
import json

from specs.feature.testutils.app import setup_app


@pytest.mark.describe('API /api/worker/download の機能テスト')
@pytest.mark.it('ダウンロード処理を開始する。')
@pytest.mark.it('ダウンロード中はSSEで進捗を通知する。')
def test_download(setup_app):
    res = requests.post('http://localhost:8000/api/worker/download')
    assert res.status_code == 200
    assert res.json() == {'status': 'ok'}

    res = requests.get('http://localhost:8000/api/sse/download', stream=True)

    for _line in res.iter_lines():
        line = _line.decode('utf-8')
        if line:
            assert line.startswith('data: ')

            if line == 'data: {}':
                continue

            data = json.loads(line[len('data: '):])
            assert data.keys() == {'target', 'total', 'progress', 'percentage', 'elapsed', 'remaining'}
            if data['percentage'] >= 100.0:
                break

    assert data['target'] == 'CompVis/stable-diffusion-v1-4/fp16'
    assert data['total'] == 10
    assert data['progress'] == 10
    assert data['percentage'] >= 100.0

