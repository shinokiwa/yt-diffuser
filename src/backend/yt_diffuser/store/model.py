""" モデルストアクラス
"""
import shutil
from sqlite3 import Connection
from pathlib import Path
from logging import getLogger; logger = getLogger(__name__)

from yt_diffuser.config import AppConfig
from yt_diffuser.store.lock import StoreLock, StoreLockedError
from yt_diffuser.store.db.op.model_info import (
    get,
    save,
    delete
)

class ModelStore:
    """ モデルストアクラス
    """
    def __init__(self, config: AppConfig,
                 model_name: str,
                 screen_name: str = None,
    ):
        self.base_dir: Path = config.STORE_MODEL_DIR
        self.model_name: str = model_name  
        self.revision: str = "main"
        self.screen_name: str = screen_name

    
    @property
    def path(self) -> Path:
        """
        モデルストアのパス
        """
        return self.base_dir / self.model_name
    
    def get_info (self, conn: Connection) -> None:
        """
        DBから追加情報を取得する。

        Args:
            conn (Connection): DBコネクション
        """
        info = get(conn, self.model_name, self.revision)
        if info is None:
            return

        self.screen_name = info['screen_name']

    
    def save_info (self, conn: Connection) -> None:
        """
        DBに追加情報を保存する。

        Args:
            conn (Connection): DBコネクション
        """
        save(conn, self.model_name, self.revision, self.__class__.__name__, self.screen_name)
        return
    
    def get_lock (self) -> StoreLock:
        """
        ロックを取得する。

        Returns:
            StoreLock: ロックオブジェクト
        """
        return StoreLock(self.path)


    def exists(self) -> bool:
        """
        ストアディレクトリが存在するかどうかを返す。

        returns:
            bool: ストアディレクトリが存在する場合はTrue
        """
        return self.path.exists()
    
    def mkdir(self) -> None:
        """
        ストアディレクトリを作成する。

        ストアディレクトリが存在していてもエラーにはならないが、
        ロックされているときは StoreLockedError が送出される。

        raises:
            StoreLockedError: ストアディレクトリがロックされている場合
        """
        if self.get_lock().is_locked():
            raise StoreLockedError(self.path)

        self.path.mkdir(parents=True, exist_ok=True)

    def to_dict (self, keys:set) -> dict:
        """
        辞書形式に変換する。

        - 存在しないキーはNoneになる。

        Args:
            keys (set): 変換するキーの集合

        Returns:
            dict: 辞書形式のオブジェクト
        """
        return {key: getattr(self, key, None) for key in keys}

