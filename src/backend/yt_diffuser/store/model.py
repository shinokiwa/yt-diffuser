""" モデルストアクラス
"""
import shutil
from sqlite3 import Connection
from pathlib import Path
from logging import getLogger; logger = getLogger(__name__)

from yt_diffuser.config import AppConfig
from yt_diffuser.store import (
    StoreLock,
    StoreLockedError,
    Store,
    MODEL_CLASS_NAME
)
from yt_diffuser.store.db.op.models import (
    is_exists,
    insert,
    update,
    delete,
    MODEL_DEFAULT_REVISION
)

class ModelStore(Store):
    """ モデルストアクラス
    """
    class_num: int = MODEL_CLASS_NAME['ModelStore']

    def __init__(self, config: AppConfig, model_name: str, revision: str  = MODEL_DEFAULT_REVISION):
        super().__init__(config, model_name)
        self.revision: str = revision
    
    @property
    def path(self) -> Path:
        """
        モデルストアのパス
        """
        return self.config.STORE_MODEL_DIR / self.store_name
    
    def save(self, conn:Connection) -> None:
        """
        モデル情報を保存する。

        モデルストアが存在しない場合はValueErrorを送出する。

        args:
            conn: DBコネクション
        """
        if not self.exists():
            raise ValueError("model store not exists")
        
        with StoreLock(self.path):

            if is_exists (conn, self.store_name, self.revision):
                update(conn, self.store_name, self.revision)
            else:
                insert(conn, model_name=self.store_name, revision=self.revision, class_name=self.class_num)

    def remove(self, conn:Connection) -> None:
        """
        モデルストアを削除する。

        ディレクトリ内のファイルを削除し、DBからも削除する。
        ロック中の場合はStoreLockedErrorを送出する。

        args:
            conn: DBコネクション

        raises:
            StoreLockedError: モデルストアがロックされている場合
        """
        if self.exists():
            lock = StoreLock(self.path)
            if lock.is_locked():
                raise StoreLockedError(self.path)

            shutil.rmtree(self.path)

        delete(conn, self.store_name, MODEL_DEFAULT_REVISION)
