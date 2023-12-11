"""
ダウンロードプロセスの制御モジュール

ダウンロードプロセスはシングルトンであり、
どこからアクセスしても同じプロセスを参照することができる。
また、ダウンロードプロセスは１つしか実行されない。

今のところHuggingFaceのモデルをダウンロードするプロセスのみを実装している。
"""

import multiprocessing
from multiprocessing.context import SpawnProcess

from yt_diffuser.config import AppConfig
from yt_diffuser.web.worker.exceptions import DuplicateProcessError
from yt_diffuser.download.main import download_procedure

_process: multiprocessing.Process = None

def is_running() -> bool:
    """
    ダウンロードプロセスが実行中かどうかを返す。

    ダウンロードプロセスが実行中の場合は実行命令は受け付けない。

    Returns:
        bool: ダウンロードプロセスが実行中の場合はTrue
    """
    return _process is not None and _process.is_alive()

def download(config:AppConfig, queue:multiprocessing.Queue, repo_id:str, revision:str) -> SpawnProcess:
    """
    ダウンロードプロセスを実行する。

    ダウンロードプロセスは１つしか実行されない。

    Args:
        repo_id (str): リポジトリID
        revision (str): リビジョン
    
    Returns:
        multiprocessing.context.SpawnProcess: ダウンロードプロセス
    
    Raises:
        DuplicateProcessError: ダウンロードプロセスが実行中の場合
    """
    global _process

    if is_running():
        raise DuplicateProcessError("download process is already running")
    
    context = multiprocessing.get_context('spawn')

    _process = context.Process(
        target=download_procedure,
        args=(config, queue, repo_id, revision),
        daemon=True
    )

    _process.start()

    return _process

def terminate() -> None:
    """
    ダウンロードプロセスを終了する。

    停止状態のプロセスを終了してもエラーにならない。
    現在は強制的に終了させている。
    ワーカー側は強制終了の可能性を考慮しておく必要がある。
    """
    global _process

    if is_running():
        _process.terminate()
        _process.join()
        _process = None
