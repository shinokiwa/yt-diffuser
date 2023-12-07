""" モデルストアクラス
"""
import shutil
from sqlite3 import Connection

from yt_diffuser.store.base import Store, AppConfig
from yt_diffuser.store.db.op.models import (
    is_exists_by_pathname,
    insert,
    update_by_pathname,
    delete_by_pathname,
    MODEL_CLASS_NAME
)

class ModelStore(Store):
    """ モデルストアクラス
    """
    class_num: int = MODEL_CLASS_NAME['ModelStore']

    def __init__(self, config: AppConfig, path: str):
        super().__init__(config, path)
    
    def set_path(self, path: str) -> None:
        self.path = self.config.STORE_MODEL_DIR / path
    
    def save(self, conn:Connection, pathname: str, filename: str, revision: str) -> None:
        """ モデル情報を保存する
        """
        if not self.exists():
            raise ValueError("model store not exists")

        if is_exists_by_pathname(conn, pathname):
            update_by_pathname(conn, pathname, filename, revision)
        else:
            insert(conn, pathname, filename, revision, self.class_num)

    def remove(self, conn:Connection) -> None:
        """ モデルストアを削除する
        ディレクトリ内のファイルを削除し、DBからも削除する
        """
        if self.exists():
            shutil.rmtree(self.path)

        delete_by_pathname(conn, str(self.path))
