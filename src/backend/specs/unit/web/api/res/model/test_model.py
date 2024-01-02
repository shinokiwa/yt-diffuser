"""
yt_diffuser.web.api.res.model のテスト
"""
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
        assert response.status_code == 200

        data = response.get_json()

        # 順番は不定なので、ソートしてから比較する
        data['models'].sort(key=lambda x: (x['model_name'], x['revision']))

        assert len(data['models']) == 4

        r = data['models'][0]
        assert r['model_name'] == "test/repo_id"
        assert r['revision'] == "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
        assert r['screen_name'] == None
        assert r['commit_hash'] == "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"

        r = data['models'][1]
        assert r['model_name'] == "test/repo_id"
        assert r['revision'] == "test_revision"
        assert r['screen_name'] == None
        assert r['commit_hash'] == "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

        r = data['models'][2]
        assert r['model_name'] == "test/repo_id2"
        assert r['revision'] == "fp16"
        assert r['screen_name'] == None
        assert r['commit_hash'] == "cccccccccccccccccccccccccccccccccccccccc"

        r = data['models'][3]
        assert r['model_name'] == "test/repo_id2"
        assert r['revision'] == "main"
        assert r['screen_name'] == None
        assert r['commit_hash'] == "cccccccccccccccccccccccccccccccccccccccc"
