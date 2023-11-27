""" constant.pyのテスト
"""
import pytest
import importlib
from unittest.mock import patch
from pathlib import Path

from yt_diffuser import constant

@pytest.mark.describe('constant.py')
@pytest.mark.it('BASE_DIRはテスト中は一時ディレクトリを指す')
def test_constant_base_dir() -> None:
    assert constant.BASE_DIR.stem == 'yt_diffuser_test'

    with patch.dict('os.environ', {'TEST': ''}):
        importlib.reload(constant)
        assert constant.BASE_DIR == Path(__file__).parents[4]

@pytest.mark.it('DATA_DIRは環境変数による上書きが可能')
def test_constant_data_dir() -> None:
    with patch.dict('os.environ', {}):
        assert constant.BASE_DIR == constant.DATA_DIR.parents[0]

    with patch.dict('os.environ', {'YT_DIFFUSER_DATA_DIR': '/test'}):
        importlib.reload(constant)
        assert constant.DATA_DIR == Path('/test')
        assert constant.STORE_DIR == Path('/test/store')

