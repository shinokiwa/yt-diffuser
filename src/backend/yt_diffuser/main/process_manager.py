""" プロセス管理モジュール

基本 start_loop() を呼び出すだけでよい。
"""
from typing import Callable
import atexit
import signal
from multiprocessing import get_context
import asyncio

from logging import getLogger; logger = getLogger(__name__)

from yt_diffuser.util.loop import loop_listener

context = get_context('spawn')

_processes = {
    "Web": {
        "target": None,
        "process": None,
        "shared_conn": None
    },
    "Worker": {
        "target": None,
        "process": None,
        "shared_conn": None
    }
}

def stop_all():
    """ 登録されたプロセスをすべて終了する
    通常は本モジュール外から呼び出す必要はない
    """
    logger.debug("Cleaning up processes...")

    for key in _processes.keys():
        if _processes[key]["process"] is not None and _processes[key]["process"].is_alive():
            _processes[key]["process"].terminate()
            _processes[key]["process"].join()
            logger.debug(f"{key} process terminated.")
        _processes[key]["process"] = None
        _processes[key]["shared_conn"] = None
        _processes[key]["target"] = None
    
    logger.debug("Cleanup completed.")

def signal_handler(signal_num, frame):
    """ 終了シグナルを受け取った場合の処理
    """
    logger.debug(f"Received signal {signal_num}")
    stop_all()
    exit(0)

def start_processes(web_procedure:Callable, worker_procedure:Callable) -> None:
    """ サブプロセスを初期化する
    """
    # プロシージャ登録
    _processes["Web"]["target"] = web_procedure
    _processes["Worker"]["target"] = worker_procedure

    _processes["Web"]["shared_conn"], _processes["Worker"]["shared_conn"] = context.Pipe()

    for key in _processes.keys():
        _processes[key]["process"] = context.Process(target=_processes[key]["target"], args=[_processes[key]["shared_conn"]])
        _processes[key]["process"].daemon = True
        _processes[key]["process"].start()

async def check_processes() -> None:
    """ サブプロセスを監視し、停止している場合再起動する。
    """
    for key in _processes.keys():
        if _processes[key]["process"] is None or _processes[key]["process"].is_alive() == False:

            logger.warning(f'{key} process is dead. Restarting...')

            _processes[key]["process"] = context.Process(target=_processes[key]["target"], args=[_processes[key]["shared_conn"]])
            _processes[key]["process"].daemon = True
            _processes[key]["process"].start()
    
    await asyncio.sleep(1)

def start_loop(web_procedure:Callable, worker_procedure:Callable) -> None:
    """ プロセスをすべて起動し、監視を開始する。
    登録するプロシージャはラムダ式やローカル関数ではなく、グローバルから参照できる関数である必要がある。

    param:
        web_procedure: Webプロセスのメインロジック
        worker_procedure: データ処理プロセスのメインロジック
    """
    try:
        # 初期化
        atexit.unregister(stop_all)
        atexit.register(stop_all)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        start_processes(web_procedure, worker_procedure)

        logger.debug("Start main loop.")
        asyncio.run(loop_listener(loop_callback=check_processes))

    except KeyboardInterrupt:
        logger.debug("KeyboardInterrupt")

    finally:
        logger.debug("Stop main loop.")
        stop_all()