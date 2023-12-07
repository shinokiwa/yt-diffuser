""" ストアの基底クラス
"""
import os
import threading
from pathlib import Path
import time

from yt_diffuser.config import AppConfig

class Store:
    config: AppConfig = None
    path: Path = ""
    lock_file_name: str = ".lock"

    def __init__(self, config: AppConfig, path: str):
        self.config = config
        self.set_path(path)
    
    def set_path(self, path: str) -> None:
        """ パスを設定する
        """
        self.path = self.config.STORE_DIR / path

    def exists(self) -> bool:
        """ ストアディレクトリが存在するかどうかを返す
        """
        return self.path.exists()
    
    def mkdir(self) -> None:
        """ ストアディレクトリを作成する
        """
        self.path.mkdir(parents=True, exist_ok=True)
    
    def is_locked(self) -> bool:
        """ ストアディレクトリがロックされているかどうかを返す
        .lockファイルが存在する場合はロックされていると判定するが、
        ファイルの最終更新時刻が3時間以上前の場合はロックされていないと判定する
        """
        lock_file = self.path / self.lock_file_name
        if not lock_file.exists():
            return False

        if lock_file.stat().st_mtime < time.time() - 60 * 60 * 3:
            lock_file.unlink()
            return False

        # ロック所有者が自身の場合はロックされていない
        with lock_file.open("r") as f:
            lock_info = f.read()
            pid, tid = lock_info.split("-")
            if pid == str(os.getpid()) and tid == str(threading.get_ident()):
                return False

        return True
    
    def lock(self) -> None:
        """ ストアディレクトリをロックする
        ロックファイルの内容はプロセスIDとスレッドID
        """
        lock_file = self.path / self.lock_file_name
        lock_file.touch()
        with lock_file.open("w") as f:
            f.write(f"{os.getpid()}-{threading.get_ident()}")


    def unlock(self, forced:bool = False):
        """ ストアディレクトリのロックを解除する
        自身と同様のプロセスIDとスレッドIDを持つロックファイルの場合のみ解除する

        args:
            forced: Trueの場合は強制的にロックを解除する
        """
        if not forced and self.is_locked():
            raise EnvironmentError(f"{self.path} is locked")

        lock_file = self.path / self.lock_file_name
        lock_file.unlink(True)
