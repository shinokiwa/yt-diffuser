"""
yt_diffuser.web.api.res.output.temp.dir のテスト
"""
import pytest

from datetime import datetime
from pathlib import Path

from flask import Flask

from yt_diffuser.config import AppConfig
from yt_diffuser.web.api.res.output.temp.dir import bp

from specs.utils.test_utils.config import make_config

@pytest.fixture
def app ():
    app = Flask(__name__)
    app.config['APP_CONFIG'] = make_config()
    app.register_blueprint(bp)
    return app

def test_get_temp (app, mocker):
    """
    test_get_temp

    it:
        - 一時保存中のファイル一覧を取得する。
        - 
    """
    mock_stream_list = mocker.patch('yt_diffuser.web.api.res.output.temp.dir.stream_list')
    def mock_stream_list_side_effect (base_dir):
        yield 'test1'
        yield 'test2'
        yield 'test3'
    mock_stream_list.side_effect = mock_stream_list_side_effect
    with app.test_client() as c:
        rv = c.get('/api/res/output/temp', headers={'Accept': 'text/event-stream'})
        assert rv.status_code == 200

        res = list(rv.response)
        assert res[0] == b'test1'
        assert res[1] == b'test2'
        assert res[2] == b'test3'


def test_post_temp (app, mocker):
    """
    post_temp

    it:
        - 一時保存中のファイルを正式に保存する。
        - 一次保存ディレクトリが存在しない場合は何もせずに終了する。
        - 一次保存ディレクトリが空の場合は何もせずに終了する。
        - 保存先のディレクトリを指定しない場合、現在時刻で作成したディレクトリに保存する。
    """
    config:AppConfig = app.config['APP_CONFIG']
    mock_glob = mocker.patch('yt_diffuser.web.api.res.output.temp.utils.Path.glob')
    mock_rename = mocker.patch('yt_diffuser.web.api.res.output.temp.utils.Path.rename')
    mock_datetime = mocker.patch('yt_diffuser.web.api.res.output.temp.utils.datetime')
    mock_datetime.now = mocker.MagicMock(return_value=datetime(2021, 1, 1, 0, 0, 0))

    with app.test_client() as c:
        # 一時保存ディレクトリが存在しない場合は何もせずに終了する。
        rv = c.post('/api/res/output/temp', json={'target': 'test'})
        assert rv.status_code == 200
        assert rv.json == {'status': 'ok'}
        assert mock_glob.call_count == 0
        assert mock_rename.call_count == 0

        # 一時保存ディレクトリが空の場合は何もせずに終了する。
        config.OUTPUT_TEMP_DIR.mkdir(parents=True, exist_ok=True)
        mock_glob.return_value = []

        rv = c.post('/api/res/output/temp', json={'target': 'test'})
        assert rv.status_code == 200
        assert rv.json == {'status': 'ok'}
        assert mock_glob.call_count == 1
        assert mock_rename.call_count == 0

        # 保存先のディレクトリを指定しない場合、現在時刻で作成したディレクトリに保存する。
        mock_glob.return_value = [Path('test1'), Path('test2')]

        rv = c.post('/api/res/output/temp', json={})
        assert rv.status_code == 200
        assert rv.json == {'status': 'ok'}
        assert mock_glob.call_count == 2
        assert mock_rename.call_count == 2
        assert mock_rename.call_args_list[0][0][0] == config.OUTPUT_IMAGE_DIR / '2021-01-01 00-00-00' / 'test1'
        assert mock_rename.call_args_list[1][0][0] == config.OUTPUT_IMAGE_DIR / '2021-01-01 00-00-00' / 'test2'

        # 保存先のディレクトリを指定した場合、指定したディレクトリに保存する。
        rv = c.post('/api/res/output/temp', json={'target': 'test'})
        assert rv.status_code == 200
        assert rv.json == {'status': 'ok'}
        assert mock_glob.call_count == 3
        assert mock_rename.call_count == 4
        assert mock_rename.call_args_list[2][0][0] == config.OUTPUT_IMAGE_DIR / 'test' / 'test1'
        assert mock_rename.call_args_list[3][0][0] == config.OUTPUT_IMAGE_DIR / 'test' / 'test2'

        # 上位ディレクトリを指定した場合はエラー
        rv = c.post('/api/res/output/temp', json={'target': '../test'})
        assert rv.status_code == 400
        assert rv.json['status'] == 'ng'
        assert rv.json['message'] == 'invalid-request'


def test_delete_temp (app, mocker):
    """
    test_delete_temp

    it:
        - 一時保存中のファイルを削除する。
    """
    config:AppConfig = app.config['APP_CONFIG']
    mock_iterdir = mocker.patch('yt_diffuser.web.api.res.output.temp.utils.Path.iterdir')
    mock_iterdir.return_value = [Path('test1'), Path('test2')]

    mock_is_dir = mocker.patch('yt_diffuser.web.api.res.output.temp.utils.Path.is_dir')
    mock_is_dir.side_effect = [False, True]

    mock_unlink = mocker.patch('yt_diffuser.web.api.res.output.temp.utils.Path.unlink')
    mock_rmtree = mocker.patch('yt_diffuser.web.api.res.output.temp.dir.shutil.rmtree')

    with app.test_client() as c:
        # 一時保存ディレクトリが存在しない場合は何もせずに終了する。
        rv = c.delete('/api/res/output/temp')
        assert rv.status_code == 200
        assert rv.json == {'status': 'ok'}
        assert mock_rmtree.call_count == 0
        assert mock_unlink.call_count == 0

        # 正常系
        config.OUTPUT_TEMP_DIR.mkdir(parents=True, exist_ok=True)
        rv = c.delete('/api/res/output/temp')
        assert rv.status_code == 200
        assert rv.json == {'status': 'ok'}
        assert mock_unlink.call_count == 1
        assert mock_rmtree.call_count == 1
        assert mock_rmtree.call_args_list[0][0][0] == Path('test2')

