""" yt_diffuser.web.worker.download のテスト
"""
import pytest
import multiprocessing
from multiprocessing.context import SpawnProcess
import time

from yt_diffuser.config import AppConfig
from yt_diffuser.web.worker.download import (
    is_running,
    download,
    terminate,
    DuplicateProcessError
)

def dummy():
    """
    ダミープロセス

    ダウンロードプロセスはグローバル領域から
    参照できるようにする必要があるため、ここで定義する。
    """
    time.sleep(5)

def test_is_running(mocker):
    """
    is_running()

    it:
        ダウンロードプロセスが実行中かどうかを返す。
    """
    mocker.patch('yt_diffuser.web.worker.download._process', None)
    assert is_running() == False

    def dummy():
        time.sleep(5)
    p = multiprocessing.Process(target=dummy)
    mocker.patch('yt_diffuser.web.worker.download._process', p)

    assert is_running() == False

    p.start()
    assert is_running() == True
    p.terminate()

def test_download(mocker):
    """
    download()

    it:
        ダウンロードプロセスを実行する。
        ダウンロードプロセスは１つしか実行されない。
    """
    mocker.patch('yt_diffuser.web.worker.download._process', None)

    mocker.patch('yt_diffuser.web.worker.download.download_procedure', dummy)

    p = download(AppConfig(), multiprocessing.Queue(), "repo_id", "revision")
    assert type(p) == SpawnProcess
    assert p.is_alive() == True

    with pytest.raises(DuplicateProcessError):
        mocker.patch('yt_diffuser.web.worker.download.is_running', return_value=True)
        download(AppConfig(), multiprocessing.Queue(), "repo_id", "revision")
    
    p.terminate()


def test_terminate(mocker):
    """ terminate()

    it:
        ダウンロードプロセスを終了する。
        停止状態のプロセスを終了してもエラーにならない。
    """

    p = multiprocessing.Process(target=dummy)
    mocker.patch('yt_diffuser.web.worker.download._process', p)
    p.start()

    terminate()
    assert p.is_alive() == False

    assert terminate() is None
