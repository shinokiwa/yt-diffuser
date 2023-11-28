""" constant.pyのテスト
"""
import pytest
from pathlib import Path

from yt_diffuser.config import AppConfig

@pytest.mark.describe('AppConfig')
class TestAppConfig:
    """ AppConfigのテスト
    """

    @pytest.mark.it('設定値を保持する')
    def test_init(self):
        c = AppConfig()

        assert c.DB_VERSION == 1
        assert c.BASE_DIR == Path(__file__).parents[4]

    @pytest.mark.it('コンストラクタ引数で一部の設定値を上書きできる')
    def test_init_with_args(self):
        c = AppConfig(BASE_DIR="test")

        assert c.BASE_DIR == Path("test")
