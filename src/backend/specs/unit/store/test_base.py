"""
yt_diffuser.store.base.Store のテスト
"""
import pytest
import tempfile
from pathlib import Path


from yt_diffuser.config import AppConfig
from yt_diffuser.store.base import Store, StoreLockedError

class TestStore:
    """
    Store のテスト
    """

    def test_path(self):
        """
        path プロパティ

        it:
            渡されたConfigからストアディレクトリのパスを生成する。
        """
        config = AppConfig()
        config.STORE_DIR = Path("/tmp")

        store = Store(config, "test")
        assert store.path == Path("/tmp/test")
    
    def test_exists(self, mocker):
        """
        exists

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
            config.STORE_DIR = Path(tmp_dir)

            store = Store(config, "test")
            assert store.exists() == False

            store.mkdir()
            assert store.exists() == True

            # ロックされている場合
            mocker.patch("yt_diffuser.store.base.StoreLock.is_locked", return_value=True)
            with pytest.raises(StoreLockedError):
                store.mkdir()

