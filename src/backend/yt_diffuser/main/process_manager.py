""" プロセス管理モジュール

基本 start_loop() を呼び出すだけでよい。
"""
import atexit
import signal
import multiprocessing
import time

from logging import getLogger; logger = getLogger(__name__)

from yt_diffuser.util.loop import infinite_loop
from yt_diffuser.web.main import web_procedure
from yt_diffuser.worker.main import worker_procedure

context = multiprocessing.get_context('spawn')

web_process = None
worker_process = None

web_send_queue = None
worker_send_queue = None

def stop_all():
    """ 登録されたプロセスをすべて終了する
    通常は本モジュール外から呼び出す必要はない
    """
    global web_process, worker_process, web_send_queue, worker_send_queue

    logger.debug("Cleaning up processes...")

    for p in [web_process, worker_process]:
        if p is not None and p.is_alive():
            p.terminate()
            p.join()
    
    web_process = None
    worker_process = None
    web_send_queue = None
    worker_send_queue = None
    
    logger.debug("Cleanup completed.")

def signal_handler(signal_num, frame):
    """ 終了シグナルを受け取った場合の処理
    """
    global web_process, worker_process, web_send_queue, worker_send_queue

    logger.debug(f"Received signal {signal_num}")
    stop_all()
    exit(0)

def start_processes() -> None:
    """ サブプロセスを初期化する
    """
    global web_process, worker_process, web_send_queue, worker_send_queue

    # プロシージャ登録
    web_send_queue = context.Queue()
    worker_send_queue = context.Queue()

    web_process = context.Process(target=web_procedure, args=[web_send_queue, worker_send_queue])
    worker_process = context.Process(target=worker_procedure, args=[worker_send_queue, web_send_queue])

    for p in [web_process, worker_process]:
        p.daemon = True
        p.start()

def check_processes() -> None:
    """ サブプロセスを監視し、停止している場合再起動する。
    """
    global web_process, worker_process, web_send_queue, worker_send_queue

    if web_process is not None and not web_process.is_alive():
        logger.debug("Web process is down. Restarting...")
        web_process = context.Process(target=web_procedure, args=[web_send_queue, worker_send_queue])
        web_process.daemon = True
        web_process.start()
    
    if worker_process is not None and not worker_process.is_alive():
        logger.debug("Worker process is down. Restarting...")
        worker_process = context.Process(target=worker_procedure, args=[worker_send_queue, web_send_queue])
        worker_process.daemon = True
        worker_process.start()

def start_loop() -> None:
    """ プロセスをすべて起動し、監視を開始する。
    登録するプロシージャはラムダ式やローカル関数ではなく、グローバルから参照できる関数である必要がある。
    """
    try:
        # 初期化
        atexit.unregister(stop_all)
        atexit.register(stop_all)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        start_processes()

        logger.debug("Start main loop.")
        infinite_loop(loop_callback=check_processes)

    except KeyboardInterrupt:
        logger.debug("KeyboardInterrupt")

    finally:
        logger.debug("Stop main loop.")
        stop_all()