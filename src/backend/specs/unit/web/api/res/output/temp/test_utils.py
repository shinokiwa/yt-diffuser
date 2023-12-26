"""
yt_diffuser.web.api.res.output.temp.utils のテスト
"""
import pytest

from pydantic import ValidationError

from specs.utils.test_utils.config import make_config
from yt_diffuser.web.api.res.output.temp.utils import *


class TestPostTempRequest:
    """
    TestPostTempRequest
    """
    def test_target(self):
        """
        target未指定時は現在時刻から生成する。
        """
        request = PostTempRequest()
        assert request.target == datetime.now().strftime('%Y-%m-%d %H-%M-%S')

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

