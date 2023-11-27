""" ストアの基底クラス
"""
from pathlib import Path
import time

from yt_diffuser.constant import STORE_DIR, STORE_LOCK_FILE

class Store:
    base_dir: Path = STORE_DIR
    path: str = ""

    def __init__(self, path: str):
        self.path = path
    
    def get_path(self) -> Path:
        """ ストアディレクトリのパスを返す
        """
        return self.base_dir / self.path
    
    def mkdir(self) -> None:
        """ ストアディレクトリを作成する
        """
        self.get_path().mkdir(parents=True, exist_ok=True)
    
    def is_locked(self) -> bool:
        """ ストアディレクトリがロックされているかどうかを返す
        .lockファイルが存在する場合はロックされていると判定するが、
        ファイルの最終更新時刻が3時間以上前の場合はロックされていないと判定する
        """
        lock_file = self.get_path() / STORE_LOCK_FILE
        if not lock_file.exists():
            return False

        if lock_file.stat().st_mtime < time.time() - 60 * 60 * 3:
            lock_file.unlink()
            return False
        
        return True
    
    def lock(self) -> None:
        """ ストアディレクトリをロックする
        """
        lock_file = self.get_path() / STORE_LOCK_FILE
        lock_file.touch()
    
    def unlock(self) -> None:
        """ ストアディレクトリのロックを解除する
        """
        lock_file = self.get_path() / STORE_LOCK_FILE
        lock_file.unlink()
