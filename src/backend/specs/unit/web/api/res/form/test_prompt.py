"""
yt_diffuser.web.api.res.form.latest のテスト
"""
import pytest
from flask import Flask

from specs.mock.web.mock_app import app
from yt_diffuser.config import AppConfig
from yt_diffuser.database import connect_database
from yt_diffuser.web.api.res.form.latest import *


def test_get_form_prompt (app:Flask):
    """
    get_form_prompt

    it:
        - プロンプトを取得する。
    """
    config:AppConfig = app.config['APP_CONFIG']

    with app.test_client() as client, \
        connect_database(config.DB_FILE) as conn:
        # データ初期化
        conn.executescript("DELETE FROM prompt_archive; UPDATE sqlite_sequence SET seq = 0 WHERE name = 'prompt_archive';")

        response = client.get('/api/res/form/prompt')
        assert response.status_code == 200

        data = response.get_json()
        assert data == {'prompts': []}

        # データを追加する
        conn.execute((
            "INSERT INTO prompt_archive (type, prompt, updated_at) VALUES "
            "('p', 'test_prompt', '2000-01-01 00:00:00'),"
            "('p', 'test_prompt2', '2001-01-01 00:00:00'),"
            "('n', 'test_n_prompt', '2000-01-01 00:00:00')"
        ))
        conn.commit()

        response = client.get('/api/res/form/prompt')
        assert response.status_code == 200
        data = response.get_json()
        assert data == {
            'prompts': [
                {'id': 2, 'prompt': 'test_prompt2'},
                {'id': 1, 'prompt': 'test_prompt'}
            ]
        }

def test_post_form_prompt (app:Flask):
    """
    put_form_prompt

    it:
        - プロンプトを新規保存する。
    """
    config:AppConfig = app.config['APP_CONFIG']

    with app.test_client() as client, \
        connect_database(config.DB_FILE) as conn:
        # データ初期化
        conn.executescript("DELETE FROM prompt_archive; UPDATE sqlite_sequence SET seq = 0 WHERE name = 'prompt_archive';")

        response = client.post('/api/res/form/prompt', json={
            'prompt': 'test_prompt'
        })
        assert response.status_code == 200

        data = response.get_json()
        assert data == {'status': 'OK'}

        result = conn.execute("SELECT * FROM prompt_archive").fetchall()
        assert len(result) == 1
        assert result[0]['type'] == 'p'
        assert result[0]['prompt'] == 'test_prompt'

def test_post_form_n_prompt (app:Flask):
    """
    get_form_n_prompt

    it:
        - ネガティブプロンプトを取得する。
    """
    config:AppConfig = app.config['APP_CONFIG']

    with app.test_client() as client, \
        connect_database(config.DB_FILE) as conn:
        # データ初期化
        conn.executescript("DELETE FROM prompt_archive; UPDATE sqlite_sequence SET seq = 0 WHERE name = 'prompt_archive';")

        response = client.post('/api/res/form/n_prompt')
        assert response.status_code == 200

        data = response.get_json()
        assert data == {'prompts': []}

        # データを追加する
        conn.execute((
            "INSERT INTO prompt_archive (type, prompt, updated_at) VALUES "
            "('p', 'test_prompt', '2000-01-01 00:00:00'),"
            "('n', 'test_n_prompt', '2000-01-01 00:00:00')"
        ))
        conn.commit()

        response = client.get('/api/res/form/n_prompt')
        assert response.status_code == 200
        data = response.get_json()
        assert data == {
            'prompts': [
                {'id': 2, 'prompt': 'test_n_prompt'}
            ]
        }

def test_post_form_n_prompt (app:Flask):
    """
    put_form_n_prompt

    it:
        - ネガティブプロンプトを保存する。
    """
    config:AppConfig = app.config['APP_CONFIG']

    with app.test_client() as client, \
        connect_database(config.DB_FILE) as conn:
        # データ初期化
        conn.executescript("DELETE FROM prompt_archive; UPDATE sqlite_sequence SET seq = 0 WHERE name = 'prompt_archive';")

        response = client.post('/api/res/form/n_prompt', json={
            'prompt': 'test_n_prompt'
        })
        assert response.status_code == 200

        data = response.get_json()
        assert data == {'status': 'OK'}

        # データを追加する
        result = conn.execute("SELECT * FROM prompt_archive").fetchall()
        assert len(result) == 1
        assert result[0]['type'] == 'n'
        assert result[0]['prompt'] == 'test_n_prompt'

def test_post_prompt_id (app:Flask):
    """
    post_prompt

    it:
        - プロンプトを更新する。
        - 今の所更新日付を更新するだけ。
    """
    config:AppConfig = app.config['APP_CONFIG']

    with app.test_client() as client, \
        connect_database(config.DB_FILE) as conn:
        # データ初期化
        conn.executescript("DELETE FROM prompt_archive; UPDATE sqlite_sequence SET seq = 0 WHERE name = 'prompt_archive';")

        # データを追加する
        conn.execute((
            "INSERT INTO prompt_archive (type, prompt, updated_at) VALUES "
            "('p', 'test_prompt', '2000-01-01 00:00:00'),"
            "('n', 'test_n_prompt', '2001-01-01 00:00:00')"
        ))
        conn.commit()

        response = client.post('/api/res/form/prompt/1')
        assert response.status_code == 200

        result = conn.execute("SELECT * FROM prompt_archive ORDER BY updated_at DESC").fetchall()
        assert len(result) == 2
        assert result[0]['type'] == 'p'
        assert result[0]['prompt'] == 'test_prompt'
        assert result[1]['type'] == 'n'
        assert result[1]['prompt'] == 'test_n_prompt'

def test_delete_prompt (app:Flask):
    """
    delete_prompt

    it:
        - プロンプトを削除する。
    """
    config:AppConfig = app.config['APP_CONFIG']

    with app.test_client() as client, \
        connect_database(config.DB_FILE) as conn:
        # データ初期化
        conn.executescript("DELETE FROM prompt_archive; UPDATE sqlite_sequence SET seq = 0 WHERE name = 'prompt_archive';")

        # データを追加する
        conn.execute((
            "INSERT INTO prompt_archive (type, prompt, updated_at) VALUES "
            "('p', 'test_prompt', '2000-01-01 00:00:00'),"
            "('n', 'test_n_prompt', '2001-01-01 00:00:00')"
        ))
        conn.commit()

        response = client.delete('/api/res/form/prompt/1')
        assert response.status_code == 200

        result = conn.execute("SELECT * FROM prompt_archive").fetchall()
        assert len(result) == 1
        assert result[0]['type'] == 'n'
        assert result[0]['prompt'] == 'test_n_prompt'