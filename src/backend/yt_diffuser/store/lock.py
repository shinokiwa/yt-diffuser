"""
ロック処理を行うモジュール
"""
from typing import Union
import os
import time
from pathlib import Path
import threading

from yt_diffuser.store.exceptions import StoreLockedError

class StoreLock:
    """
    ストアのロックを行うクラス

    with StoreLock() でロックが取得できる。
    """

    lock_file_name = ".lock"

    def __init__ (self, path: Union[str, Path]):
        """
        コンストラクタ

        args:
            path: ロックファイルを作成するディレクトリのパス
        """
        self.path:Path = Path(path)

    @property
    def lock_file(self) -> Path:
        """
        ロックファイルのパスを返す。
        """
        return self.path / self.__class__.lock_file_name

    def is_locked(self, ignore_owner:bool = False) -> bool:
        """
        ストアディレクトリがロックされているかどうかを返す。

        .lockファイルが存在する場合はロックされていると判定するが、
        以下のいずれかの条件に合致した場合はロックされていないと判定する。
        - ファイルの最終更新時刻が3時間以上前の場合
        - ロックファイルの所有者が自身の場合

        args:
            ignore_owner: Trueの場合はロックファイルの所有者が自身の場合もロックされていると判定する

        returns:
            bool: ロックされている場合はTrue
        """
        lock_file = self.lock_file

        # ロックファイルが存在しない場合はロックされていない
        if not lock_file.exists():
            return False

        # ロックファイルの最終更新時刻が3時間以上前の場合はロックされていない
        if lock_file.stat().st_mtime < time.time() - 60 * 60 * 3:
            lock_file.unlink()
            return False

        # 所有者を無視する場合はここで終了
        if ignore_owner:
            return True

        # ロック所有者が自身の場合はロックされていない
        with lock_file.open("r") as f:
            lock_info = f.read()
            pid, tid = lock_info.split("-")
            if pid == str(os.getpid()) and tid == str(threading.get_ident()):
                return False

        return True

    
    def acquire(self):
        """
        ストアディレクトリをロックする。

        ロックファイルの内容は{プロセスID}-{スレッドID}とする。
        
        raises:
            StoreLockedError: ロック済みの場合
        """
        if self.is_locked():
            raise StoreLockedError(self.path)

        lock_file = self.lock_file
        lock_file.touch()
        with lock_file.open("w") as f:
            f.write(f"{os.getpid()}-{threading.get_ident()}")


    def release(self, force:bool = False):
        """
        ストアディレクトリのロックを解除する。

        ロックファイルが自身と同様のプロセスIDとスレッドIDを持つ場合のみ解除する。

        args:
            force: Trueの場合は強制的にロックを解除する
        """
        if not force and self.is_locked():
            raise StoreLockedError(self.path)

        lock_file = self.lock_file
        lock_file.unlink(missing_ok=True)
    
    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()
