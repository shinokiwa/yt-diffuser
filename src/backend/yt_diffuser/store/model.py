""" モデルストアクラス
"""
import shutil
from sqlite3 import Connection
from logging import getLogger; logger = getLogger(__name__)

from yt_diffuser.store.base import Store, AppConfig
from yt_diffuser.store.db.op.models import (
    is_exists,
    insert,
    update,
    delete,
    MODEL_CLASS_NAME
)

class ModelStore(Store):
    """ モデルストアクラス
    """
    class_num: int = MODEL_CLASS_NAME['ModelStore']

    def __init__(self, config: AppConfig, path: str, revision: str):
        super().__init__(config, path)
        self.revision:str = revision
    
    def set_path(self, path: str) -> None:
        self.path = self.config.STORE_MODEL_DIR / path
    
    def save(self, conn:Connection) -> None:
        """ モデル情報を保存する
        """
        if not self.exists():
            raise ValueError("model store not exists")

        if is_exists_by_pathname(conn, self.path, self.revision):
            update_by_pathname(conn, self.path, self.revision, name="")
        else:
            insert(conn, model_name=self.path, revision=self.revision, name="", class_name=self.class_num)

    def remove(self, conn:Connection) -> None:
        """ モデルストアを削除する
        ディレクトリ内のファイルを削除し、DBからも削除する
        """
        if self.exists():
            shutil.rmtree(self.path)

        delete_by_pathname(conn, self.path, self.revision)
