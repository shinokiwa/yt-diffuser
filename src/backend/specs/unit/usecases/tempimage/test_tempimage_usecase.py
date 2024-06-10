import pytest
from pytest_mock import MockerFixture

import tempfile
from pathlib import Path

from yt_diffuser.types.path import AppPath
from yt_diffuser.usecases.web.tempimage.tempimage_usecase import TempImageUseCase

class TestTempImageUseCase:
    """
    TempImageUseCase

    一時保存画像のユースケース
    """

    def test_get_index(self, mocker):
        """
        get_index

        it:
            - 一時保存画像の一覧を取得する
        """
        pt = AppPath(base_dir=tempfile.mkdtemp())
        usecase = TempImageUseCase(pt)

        result = usecase.get_index()

        assert pt.OUTPUT_TEMP_DIR.exists() == True, "一時保存ディレクトリが存在しない場合、ディレクトリを作成する。"
        assert result == [], "ディレクトリが空の場合、空のリストを返す。"

        pt.OUTPUT_TEMP_DIR.joinpath('test1.jpg').touch()
        pt.OUTPUT_TEMP_DIR.joinpath('test2.jpg').touch()
        pt.OUTPUT_TEMP_DIR.joinpath('test3.jpg').touch()

        result = usecase.get_index()
        result = sorted(result)

        assert result == ['test1.jpg', 'test2.jpg', 'test3.jpg'], "ディレクトリ内のファイル一覧を返す。"