"""
yt_diffuser.web.api.res.form.latest のテスト
"""
from flask import Flask

from specs.mock.web.mock_app import app
from yt_diffuser.config import AppConfig
from yt_diffuser.database import connect_database
from yt_diffuser.web.api.res.form.latest import bp

def test_get_form_latest (app:Flask):
    """
    get_form_latest

    it:
        - 最後にフォームに入力した値を取得する。
        - ついでに不要なレコードを削除する。
    """
    config:AppConfig = app.config['APP_CONFIG']

    with app.test_client() as client, \
        connect_database(config.DB_FILE) as conn:
        response = client.get('/api/res/form/latest')
        assert response.status_code == 200

        data = response.get_json()
        assert data == {}

        # データを追加する
        conn.execute((
            "INSERT INTO form_data (name, value) VALUES "
            "('base_model', 'test/repo_id'),"
            "('base_model_revision', 'test_revision'),"
            "('prompt', 'test_prompt'),"
            "('negative_prompt', 'test_n_prompt'),"
            "('invalid', 'test_invalid')"
        ))
        conn.commit()

        response = client.get('/api/res/form/latest')
        assert response.status_code == 200
        data = response.get_json()
        assert data == {
            'base_model': 'test/repo_id',
            'base_model_revision': 'test_revision',
            'prompt': 'test_prompt',
            'negative_prompt': 'test_n_prompt'
        }

        rec = conn.execute("SELECT * FROM form_data WHERE name = 'invalid'").fetchall()
        assert len(rec) == 0

def test_post_form_latest (app:Flask):
    """
    post_form_latest

    it:
        - 最後にフォームに入力した値を保存する。
    """
    config:AppConfig = app.config['APP_CONFIG']

    with app.test_client() as client, \
        connect_database(config.DB_FILE) as conn:
        response = client.post('/api/res/form/latest', json={
            'base_model': 'test/repo_id',
            'base_model_revision': 'test_revision',
            'prompt': 'test_prompt',
            'negative_prompt': 'test_n_prompt'
        })
        assert response.status_code == 200

        # データが保存されていることを確認する
        cursor = conn.execute("SELECT * FROM form_data")
        data = cursor.fetchall()
        assert len(data) == 4

        assert data[0]['name'] == 'base_model'
        assert data[0]['value'] == 'test/repo_id'

        assert data[1]['name'] == 'base_model_revision'
        assert data[1]['value'] == 'test_revision'

        assert data[2]['name'] == 'prompt'
        assert data[2]['value'] == 'test_prompt'

        assert data[3]['name'] == 'negative_prompt'
        assert data[3]['value'] == 'test_n_prompt'

        # Noneは保存されない
        response = client.post('/api/res/form/latest', json={
            'base_model': 'test/repo_id',
            'base_model_revision': None,
            'prompt': None,
            'negative_prompt': None
        })
        assert response.status_code == 200

        # データが保存されていることを確認する
        cursor = conn.execute("SELECT * FROM form_data")
        data = cursor.fetchall()
        assert len(data) == 4

        assert data[0]['name'] == 'base_model'
        assert data[0]['value'] == 'test/repo_id'

        assert data[1]['name'] == 'base_model_revision'
        assert data[1]['value'] == 'test_revision'

        assert data[2]['name'] == 'prompt'
        assert data[2]['value'] == 'test_prompt'

        assert data[3]['name'] == 'negative_prompt'
        assert data[3]['value'] == 'test_n_prompt'

        # 無関係なデータは保存されない
        response = client.post('/api/res/form/latest', json={
            'base_model': 'test/repo_id',
            'base_model_revision': 'test_revision',
            'prompt': 'test_prompt',
            'negative_prompt': 'test_n_prompt',
            'invalid': 'test_invalid'
        })
        assert response.status_code == 200

        # データが保存されていることを確認する
        cursor = conn.execute("SELECT * FROM form_data WHERE name = 'invalid'")
        data = cursor.fetchall()
        assert len(data) == 0
