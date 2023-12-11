"""
yt_diffuser.store.lock のテスト
"""
import pytest
import os
import time
import threading
import multiprocessing
import tempfile
from pathlib import Path

from yt_diffuser.store.lock import StoreLock, StoreLockedError

class TestStoreLock:
    """
    StoreLock のテスト
    """
    
    def test_lock_file(self):
        """
        lock_file プロパティ

        ロックファイルのパスを返す。
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            store_lock = StoreLock(tmp_dir)
            assert store_lock.lock_file == Path(store_lock.path) / ".lock"
    
    def test_is_locked(self):
        """
        is_locked

        it:
            ストアディレクトリにロックファイルが存在する場合はTrueを返す。
            ロックファイルが存在していても、最終更新時刻が3時間以上前の場合はFalseを返す。
            ロックファイルの所有者が自身の場合はFalseを返す。
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            store_lock = StoreLock(tmp_dir)

            assert store_lock.is_locked() == False

            lock_file = store_lock.lock_file

            # ロック所有者が他者の場合
            f = lock_file.open("w")
            f.write("0-0")
            f.close()
            assert store_lock.is_locked() == True

            # ロックファイルの最終更新時刻が3時間以上前の場合
            os.utime(lock_file, (time.time() - 60 * 60 * 3 - 1, time.time() - 60 * 60 * 3 - 1))
            assert store_lock.is_locked() == False

            # ロックファイルの所有者が自身の場合
            f = lock_file.open("w")
            f.write(f"{os.getpid()}-{threading.get_ident()}")
            f.close()

            assert store_lock.is_locked() == False

            # 所有者を無視する場合
            assert store_lock.is_locked(ignore_owner=True) == True

            lock_file.unlink()
            assert store_lock.is_locked() == False
    
    def test_lock(self):
        """
        acquire
        release

        it:
            ロックを取得する。
            with ステートメントで実行可能。
            ロック済みの場合は例外を送出する。

        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            with StoreLock(tmp_dir) as store_lock:
                assert store_lock.is_locked() == False
                assert store_lock.is_locked(ignore_owner=True) == True

                # ロック済みの場合は例外を送出する。
                def other_thread():
                    assert store_lock.is_locked() == True
                    assert store_lock.is_locked(ignore_owner=True) == True
                    with pytest.raises(StoreLockedError):
                        store_lock.acquire()

                    with pytest.raises(StoreLockedError):
                        store_lock.release()
                
                t = threading.Thread(target=other_thread)
                t.start()
                t.join()

                mp = multiprocessing.Process(target=other_thread)
                mp.start()
                mp.join()

            # with ステートメントを抜けるとロックが解除される。
            assert store_lock.is_locked() == False
            assert store_lock.is_locked(ignore_owner=True) == False
            assert store_lock.lock_file.exists() == False

            # force付きのrelaseで強制的にロックを解除できる。
            with store_lock:
                assert store_lock.is_locked() == False
                assert store_lock.is_locked(ignore_owner=True) == True

                def other_thread():
                    assert store_lock.is_locked() == True
                    assert store_lock.is_locked(ignore_owner=True) == True
                    store_lock.release(force=True)
                
                t = threading.Thread(target=other_thread)
                t.start()
                t.join()

                assert store_lock.is_locked() == False
                assert store_lock.is_locked(ignore_owner=True) == False
                assert store_lock.lock_file.exists() == False
