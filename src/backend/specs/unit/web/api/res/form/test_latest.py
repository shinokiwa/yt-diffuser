"""
yt_diffuser.web.api.res.form.latest のテスト
"""
import pytest
from flask import Flask

from specs.mock.web.mock_app import app
from yt_diffuser.config import AppConfig
from yt_diffuser.database import connect_database
from yt_diffuser.web.api.res.form.latest import bp, FormData

@pytest.fixture(scope='function')
def conn (app:Flask):
    """
    テスト用のDBコネクションを取得し、ついでにテーブルも整理
    """
    config:AppConfig = app.config['APP_CONFIG']
    conn = connect_database(config.DB_FILE)
    conn.execute("DELETE FROM form_data")
    conn.commit()
    yield conn
    conn.execute("DELETE FROM form_data")
    conn.commit()

class TestFormData:
    """
    FormData
    """

    def test_compile_to_bool (self):
        """
        compile_to_bool

        it:
            - compileはboolまたは'1'/'0'を受け付けて、boolに変換する。
        """
        assert FormData.compile_to_bool(True) == True
        assert FormData.compile_to_bool(False) == False
        assert FormData.compile_to_bool('1') == True
        assert FormData.compile_to_bool('0') == False

        with pytest.raises(ValueError):
            FormData.compile_to_bool('invalid')


def test_get_form_latest (app:Flask, conn):
    """
    get_form_latest

    it:
        - 最後にフォームに入力した値を取得する。
        - ついでに不要なレコードを削除する。
    """
    with app.test_client() as client:
        # 空の場合
        response = client.get('/api/res/form/latest')
        assert response.status_code == 200

        data = response.get_json()
        assert data == {
            'base_model_name': None,
            'base_model_revision': None,
            'lora_model_name': None,
            'lora_model_revision': None,
            'lora_model_weight': None,
            'controlnet_model_name': None,
            'controlnet_model_revision': None,
            'controlnet_model_weight': None,
            'compile': None,
            'seed': None,
            'width': None,
            'height': None,
            'prompt': None,
            'negative_prompt': None,
            'scheduler': None,
            'inference_steps': None,
            'guidance_scale': None,
            'memo': None
        }

        # データを追加する
        conn.execute((
            "INSERT INTO form_data (name, value) VALUES "
            "('base_model_name', 'test/repo_id'),"
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
            'base_model_name': 'test/repo_id',
            'base_model_revision': 'test_revision',
            'lora_model_name': None,
            'lora_model_revision': None,
            'lora_model_weight': None,
            'controlnet_model_name': None,
            'controlnet_model_revision': None,
            'controlnet_model_weight': None,
            'compile': None,
            'seed': None,
            'width': None,
            'height': None,
            'prompt': 'test_prompt',
            'negative_prompt': 'test_n_prompt',
            'scheduler': None,
            'inference_steps': None,
            'guidance_scale': None,
            'memo': None
        }

        rec = conn.execute("SELECT * FROM form_data WHERE name = 'invalid'").fetchall()
        assert len(rec) == 0

        # 不正な値が入っている場合はエラーになる
        conn.execute("INSERT INTO form_data (name, value) VALUES ('width', 'invalid')")
        conn.commit()
        response = client.get('/api/res/form/latest')
        assert response.status_code == 500

def test_post_form_latest (app:Flask, conn):
    """
    post_form_latest

    it:
        - 最後にフォームに入力した値を保存する。
    """
    with app.test_client() as client:
        response = client.post('/api/res/form/latest', json={
            'base_model_name': 'test/repo_id',
            'base_model_revision': 'test_revision',
            'prompt': 'test_prompt',
            'negative_prompt': 'test_n_prompt'
        })
        assert response.status_code == 200

        # データが保存されていることを確認する
        cursor = conn.execute("SELECT * FROM form_data")
        data = cursor.fetchall()
        assert len(data) == 4

        assert data[0]['name'] == 'base_model_name'
        assert data[0]['value'] == 'test/repo_id'

        assert data[1]['name'] == 'base_model_revision'
        assert data[1]['value'] == 'test_revision'

        assert data[2]['name'] == 'prompt'
        assert data[2]['value'] == 'test_prompt'

        assert data[3]['name'] == 'negative_prompt'
        assert data[3]['value'] == 'test_n_prompt'

        # Noneは保存されない
        response = client.post('/api/res/form/latest', json={
            'base_model_name': 'test/repo_id',
            'base_model_revision': None,
            'prompt': None,
            'negative_prompt': None
        })
        assert response.status_code == 200

        # データが保存されていることを確認する
        cursor = conn.execute("SELECT * FROM form_data ORDER BY name")
        data = cursor.fetchall()
        assert len(data) == 4

        assert data[0]['name'] == 'base_model_name'
        assert data[0]['value'] == 'test/repo_id'

        assert data[1]['name'] == 'base_model_revision'
        assert data[1]['value'] == 'test_revision'

        assert data[2]['name'] == 'negative_prompt'
        assert data[2]['value'] == 'test_n_prompt'

        assert data[3]['name'] == 'prompt'
        assert data[3]['value'] == 'test_prompt'

        # 不正なキーが入っている場合は保存されない
        response = client.post('/api/res/form/latest', json={
            'base_model_name': 'test/repo_id',
            'base_model_revision': 'test_revision',
            'prompt': 'test_prompt',
            'negative_prompt': 'test_n_prompt',
            'invalid': 'test_invalid'
        })
        assert response.status_code == 200

        # データが保存されていないことを確認する
        cursor = conn.execute("SELECT * FROM form_data WHERE name = 'invalid'")
        data = cursor.fetchall()
        assert len(data) == 0

        # 型が不正な場合は保存されない
        response = client.post('/api/res/form/latest', json={
            'width': 'invalid'
        })
        assert response.status_code == 400

        # 空の場合は何も保存されない
        response = client.post('/api/res/form/latest', json={})
        assert response.status_code == 400
        data = response.get_json()
        assert data == {'result': 'no data'}