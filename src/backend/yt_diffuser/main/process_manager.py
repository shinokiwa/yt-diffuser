from typing import Callable
import atexit
import signal
from multiprocessing import get_context

from logging import getLogger; logger = getLogger(__name__)

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

_parent_conn = None
_child_conn = None

def stop_all():
    """ 登録されたプロセスをすべて終了する
    通常は本モジュール外から呼び出す必要はない
    """
    global _parent_conn, _child_conn

    logger.debug("Cleaning up processes...")

    for key in _processes.keys():
        if _processes[key]["process"] is not None and _processes[key]["process"].is_alive():
            _processes[key]["process"].terminate()
            _processes[key]["process"].join()
            logger.debug(f"{key} process terminated.")
        _processes[key]["process"] = None
        _processes[key]["shared_conn"] = None
        _processes[key]["target"] = None
    
    _parent_conn = None
    _child_conn = None
    
    logger.debug("Cleanup completed.")

def signal_handler(signal_num, frame):
    """ 終了シグナルを受け取った場合の処理
    """
    logger.debug(f"Received signal {signal_num}")
    stop_all()
    exit(0)


def start_all(web_procedure:Callable, worker_procedure:Callable) -> None:
    """ プロセスをすべて起動し、監視を開始する。
    登録するプロシージャはラムダ式やローカル関数ではなく、グローバルから参照できる関数である必要がある。

    param:
        web_procedure: Webプロセスのメインロジック
        worker_procedure: データ処理プロセスのメインロジック
    """
    global _parent_conn, _child_conn

    try:
        # 初期化
        atexit.unregister(stop_all)
        atexit.register(stop_all)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        # プロシージャ登録
        _processes["Web"]["target"] = web_procedure
        _processes["Worker"]["target"] = worker_procedure

        _parent_conn, _child_conn = context.Pipe()
        _processes["Web"]["shared_conn"], _processes["Worker"]["shared_conn"] = context.Pipe()

        for key in _processes.keys():
            _processes[key]["process"] = context.Process(target=_processes[key]["target"], args=(_processes[key]["shared_conn"], _child_conn))
            _processes[key]["process"].daemon = True
            _processes[key]["process"].start()

        # サブプロセスからparent_queueを通して終了要求があるまでは、サブプロセスを監視し、停止している場合再起動する。
        # 再起動要求も可能
        logger.debug("Start main loop.")
        while True:
            try:
                if _parent_conn.poll(timeout=1):
                    msg = _parent_conn.recv()
                    logger.debug(f"Received pipe signal {msg}")
                    if msg == "exit":
                        return

            except EOFError:
                pass
            
            for key in _processes.keys():
                if _processes[key]["process"] is None or _processes[key]["process"].is_alive() == False:
                    logger.warning(f'{key} process is dead. Restarting...')
                    _processes[key]["process"] = context.Process(target=_processes[key]["target"], args=(_processes[key]["shared_conn"], _child_conn))
                    _processes[key]["process"].daemon = True
                    _processes[key]["process"].start()

    except KeyboardInterrupt:
        logger.debug("KeyboardInterrupt")

    finally:
        logger.debug("Stop main loop.")
        stop_all()