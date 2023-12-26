"""
yt_diffuser.web.api.res.output.temp のテスト
"""
import pytest
import shutil

from flask import Flask
from pydantic import ValidationError

from specs.utils.test_utils.config import make_config

from yt_diffuser.web.api.res.output.temp import *

@pytest.fixture
def app ():
    app = Flask(__name__)
    app.config['APP_CONFIG'] = make_config()
    app.register_blueprint(bp)
    return app

class TestPostTempRequest:
    """
    TestPostTempRequest
    """

    def test_get_full_target (self):
        """
        test_get_full_target

        it:
            - ターゲットのフルパスを取得する。
            - ターゲットがベースディレクトリより上にある場合はエラーを返す。
        """
        request = PostTempRequest(target='test')
        base_dir = Path('/tmp')
        assert request.get_full_target(base_dir) == Path('/tmp/test')

        with pytest.raises(ValidationError):
            request = PostTempRequest(target='../test')
            request.get_full_target(base_dir)


def test_get_temp_file_path ():
    """
    test_get_temp_file_path

    it:
        - subpathから一時保存中ファイルのフルパスを取得する。
        - 共通チェックも兼ねる。
    """
    config = make_config()
    base_dir = config.OUTPUT_TEMP_DIR

    # ファイルが存在しない場合はエラー
    with pytest.raises(ValueError):
        get_temp_file_path(base_dir, 'test')
    
    # ファイルでない場合はエラー
    base_dir.mkdir(parents=True, exist_ok=True)
    (base_dir / 'test2').mkdir()

    with pytest.raises(ValueError):
        get_temp_file_path(base_dir, 'test2')
    
    # subpathがベースディレクトリより上にある場合はエラー
    with pytest.raises(ValueError):
        get_temp_file_path(base_dir, '../test3')
    
    # 正常系
    (base_dir / 'test4').touch()

    assert get_temp_file_path(base_dir, 'test4') == base_dir / 'test4'


def test_get_temp (app, mocker):
    """
    test_get_temp

    it:
        - 一時保存中のファイル一覧を取得する。
        - 
    """
    mock_stream_list = mocker.patch('yt_diffuser.web.api.res.output.temp.stream_list')
    mock_stream_list.side_effect = [
        'test1',
        'test2',
        'test3',
    ]
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
    mock_glob = mocker.patch('yt_diffuser.web.api.res.output.temp.Path.glob')
    mock_iterdir = mocker.patch('yt_diffuser.web.api.res.output.temp.Path.iterdir')
    mock_rename = mocker.patch('yt_diffuser.web.api.res.output.temp.Path.rename')

    with app.test_client() as c:
        # 一時保存ディレクトリが存在しない場合は何もせずに終了する。
        rv = c.post('/api/res/output/temp', json={'target': 'test'})

        assert rv.status_code == 200
        assert rv.json == {'status': 'ok'}
