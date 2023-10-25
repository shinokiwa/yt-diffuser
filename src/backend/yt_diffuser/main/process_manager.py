from typing import Callable
import atexit
import signal
from multiprocessing import Process, Pipe

from logging import getLogger; logger = getLogger(__name__)

_targets = {
    "web": None,
    "processing": None
}

_procs = {
    "web": None,
    "processing": None
}

_conns = {
    "parent": None,
    "child": None,
    "shared1": None,
    "shared2": None
}

@atexit.register
def cleanup():
    """ 登録されたプロセスをすべて終了する
    通常は本モジュール外から呼び出す必要はない
    """
    logger.debug("Cleaning up processes...")

    for key, p in _procs.items():
        if p is not None and p.is_alive():
            p.terminate()
            p.join()
            logger.debug(f"{key} process terminated.")
        _procs[key] = None
    
    for key, conn in _conns.items():
        if conn is not None:
            conn.close()
            logger.debug(f"{key} connection closed.")
        _conns[key] = None
    
    for key, target in _targets.items():
        _targets[key] = None

def init(web_main:Callable, processing_main:Callable) -> None:
    """ プロセス管理の初期化

    param:
        web_main: Webプロセスのメイン処理
        processing_main: データ処理プロセスのメイン処理
    """
    logger.debug("Initialize process manager.")

    cleanup()

    _targets["web"] = web_main
    _targets["processing"] = processing_main

    # メインプロセスとの通信用パイプ
    _conns["parent"], _conns["child"] = Pipe()

    # プロセス間通信用パイプ
    _conns["shared1"], _conns["shared2"] = Pipe()

    _procs["web"] = Process(target=_targets["web"], args=(_conns["shared1"], _conns["child"]))
    _procs["web"].daemon = True

    _procs["processing"] = Process(target=_targets["processing"], args=(_conns["shared2"], _conns["child"]))
    _procs["processing"].daemon = True

def signal_handler(signal_num, frame):
    """ 終了シグナルを受け取った場合の処理
    """
    logger.debug(f"Received signal {signal_num}")
    cleanup()
    exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def start_all()->None:
    """ 登録されたプロセスをすべて起動し、監視を開始する
    """
    if _procs["web"] is None or _procs["processing"] is None:
        raise Exception("Process manager is not initialized.")

    try:
        _procs["web"].start()
        _procs["processing"].start()

        # サブプロセスからparent_queueを通して終了要求があるまでは、サブプロセスを監視し、停止している場合再起動する。
        # 再起動要求も可能
        while True:
            try:
                if _conns["parent"].poll(timeout=1):
                    msg = _conns["parent"].recv()
                    if msg == "exit":
                        return

            except EOFError:
                pass
            
            if not _procs["web"].is_alive():
                logger.warning('Web process is dead. Restarting...')
                _procs["web"] = Process(target=_targets["web"], args=(_conns["shared1"], _conns["child"]))
                _procs["web"].daemon = True
                _procs["web"].start()
            
            if not _procs["processing"].is_alive():
                logger.warning('Processing process is dead. Restarting...')
                _procs["processing"] = Process(target=_targets["processing"], args=(_conns["shared2"], _conns["child"]))
                _procs["processing"].daemon = True
                _procs["processing"].start()

    except KeyboardInterrupt:
        logger.debug("KeyboardInterrupt")

    finally:
        cleanup()