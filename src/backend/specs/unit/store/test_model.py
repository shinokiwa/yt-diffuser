"""
yt_diffuser.store.model のテスト
"""
import pytest
import tempfile
from pathlib import Path

from yt_diffuser.store.model import ModelStore, AppConfig, StoreLockedError

class TestModelStore:
    """
    ModelStore のテスト
    """
    
    def test_path(self):
        """
        path プロパティ
        """
        config = AppConfig()
        store = ModelStore(config, "test")
        assert store.path == Path(config.STORE_MODEL_DIR, "test")
    
    def test_get_info(self, mocker):
        """
        get_info

        it:
            DBから追加情報を取得する。
        """
        config = AppConfig()
        store = ModelStore(config, "test")
        mock_get = mocker.patch("yt_diffuser.store.model.get", return_value={"screen_name": "test"})
        conn = "conn"

        store.get_info(conn)
        assert store.screen_name == "test"

    def test_exists(self, mocker):
        """
        exists

        TODO: mkdirとテストが混ざってる

        it:
            ストアディレクトリが存在する場合はTrueを返す。
            ストアディレクトリが存在しない場合はFalseを返す。

        mkdir

        it:
            ストアディレクトリを作成する。
            ストアディレクトリが存在していてもエラーにはならないが、
            ロックされているときは StoreLockedError が送出される。
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            config = AppConfig()
            config.STORE_MODEL_DIR = Path(tmp_dir)

            store = ModelStore(config, "test")
            assert store.exists() == False

            store.mkdir()
            assert store.exists() == True

            # ロックされている場合
            mocker.patch("yt_diffuser.store.model.StoreLock.is_locked", return_value=True)
            with pytest.raises(StoreLockedError):
                store.mkdir()