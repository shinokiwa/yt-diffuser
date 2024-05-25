"""
yt_diffuser.web.api.res.output.temp.file のテスト
"""
import pytest

from flask import Flask

from specs.mock.web.mock_app import app
from yt_diffuser.web.api.res.output.temp.file import *

def test_get_temp_file (app, mocker):
    """
    test_get_temp_file

    it:
        - 一時保存リソースの情報を取得する。
        - 現在未実装
    """
    config:AppConfig = app.config['APP_CONFIG']
    with app.test_client() as c:
        rv = c.get('/api/res/output/temp/test')
        assert rv.status_code == 400
        assert rv.json['status'] == 'ng'

        config.OUTPUT_TEMP_DIR.mkdir(parents=True, exist_ok=True)
        (config.OUTPUT_TEMP_DIR / 'test' ).touch()

        rv = c.get('/api/res/output/temp/test')
        assert rv.status_code == 200
        assert rv.json['status'] == 'ok'


def test_post_temp_file(app, mocker):
    """
    test_post_temp_file

    it:
        - 一時保存リソースを正式に保存する。
    """
    config:AppConfig = app.config['APP_CONFIG']
    with app.test_client() as c:
        rv = c.post('/api/res/output/temp/test', json={'target': 'test_dir'})
        assert rv.status_code == 400
        assert rv.json['status'] == 'ng'

        rv = c.post('/api/res/output/temp/test', json={'target': '../test_dir'})
        assert rv.status_code == 400
        assert rv.json['status'] == 'ng'

        config.OUTPUT_TEMP_DIR.mkdir(parents=True, exist_ok=True)
        (config.OUTPUT_TEMP_DIR / 'test' ).touch()

        rv = c.post('/api/res/output/temp/test', json={'target': 'test_dir'})
        assert rv.status_code == 200
        assert rv.json['status'] == 'ok'
        assert not (config.OUTPUT_TEMP_DIR / 'test').exists()
        assert (config.OUTPUT_IMAGE_DIR / 'test_dir/test').exists()


def test_delete_temp_file(app, mocker):
    """
    test_delete_temp_file

    it:
        - 一時保存ファイルを削除する。
    """
    config:AppConfig = app.config['APP_CONFIG']
    with app.test_client() as c:
        rv = c.delete('/api/res/output/temp/test')
        assert rv.status_code == 400
        assert rv.json['status'] == 'ng'

        config.OUTPUT_TEMP_DIR.mkdir(parents=True, exist_ok=True)
        (config.OUTPUT_TEMP_DIR / 'test' ).touch()

        rv = c.delete('/api/res/output/temp/test')
        assert rv.status_code == 200
        assert rv.json['status'] == 'ok'
        assert not (config.OUTPUT_TEMP_DIR / 'test').exists()