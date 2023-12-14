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
    
    def test_save(self, mocker):
        """
        save

        it:
            モデルストアが存在しない場合はValueErrorを送出する
            モデルストアが存在する場合はDBに保存する
        """
        config = AppConfig(BASE_DIR=Path(tempfile.mkdtemp()))
        store = ModelStore(config, "test")
        conn = mocker.MagicMock()
        mock_is_exists = mocker.patch("yt_diffuser.store.model.is_exists")
        mock_update = mocker.patch("yt_diffuser.store.model.update")
        mock_insert = mocker.patch("yt_diffuser.store.model.insert")

        # モデルストアが存在しない場合はValueErrorを送出する
        with pytest.raises(ValueError):
            store.save(conn)
        
        # モデルストアが存在する場合はDBに保存する
        store.path.mkdir(parents=True, exist_ok=True)
        mock_is_exists.return_value = False
        store.save(conn)

        assert mock_insert.call_count == 1
        assert mock_update.call_count == 0

        mock_is_exists.return_value = True
        store.save(conn)

        assert mock_insert.call_count == 1
        assert mock_update.call_count == 1

    def test_remove(self, mocker):
        """
        remove

        it:
            モデルストアが存在する場合は削除する
        """
        config = AppConfig(BASE_DIR=Path(tempfile.mkdtemp()))
        store = ModelStore(config, "test")
        conn = mocker.MagicMock()
        mock_store_lock = mocker.patch("yt_diffuser.store.model.StoreLock")
        mock_remove = mocker.patch("yt_diffuser.store.model.shutil.rmtree")
        mock_delete = mocker.patch("yt_diffuser.store.model.delete")

        # モデルストアが存在しない場合はDBだけ削除する
        store.remove(conn)
        assert mock_remove.call_count == 0
        assert mock_delete.call_count == 1

        # モデルストアがロックされている場合はStoreLockedErrorを送出する
        store.path.mkdir(parents=True, exist_ok=True)
        mock_store_lock.return_value.is_locked.return_value = True
        with pytest.raises(StoreLockedError):
            store.remove(conn)

        # モデルストアが存在する場合は削除する
        mock_store_lock.return_value.is_locked.return_value = False
        store.remove(conn)
        assert mock_remove.call_count == 1
        assert mock_delete.call_count == 2