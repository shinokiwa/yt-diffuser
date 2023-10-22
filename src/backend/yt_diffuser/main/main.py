""" メインプロセスのメイン処理
"""
from typing import Callable
import os , sys, subprocess
from multiprocessing import Process, Pipe
from logging import getLogger; logger = getLogger(__name__)

def process (web_main:Callable, processing_main:Callable) -> None:
    """ メインプロセス

    param:
        web_main: Webプロセスのメイン処理
        processing_main: データ処理プロセスのメイン処理
    """
    # メインプロセスとの通信用パイプ
    parent_conn, child_conn = Pipe()

    # プロセス間通信用パイプ
    shared_conn1, shared_conn2 = Pipe()

    # Webプロセスを起動
    web_proc = Process(target=web_main, args=(shared_conn1, child_conn))
    web_proc.start()

    # データ処理プロセスを起動
    processing_proc = Process(target=processing_main, args=(shared_conn2, child_conn))
    processing_proc.start()

    # サブプロセスからparent_queueを通して終了要求があるまでは、サブプロセスを監視し、停止している場合再起動する。
    while True:
        try:
            if parent_conn.poll(timeout=1):
                msg = parent_conn.recv()
                if msg == "exit":
                    return

            if not web_proc.is_alive():
                logger.warning('Web process is dead. Restarting...')
                if os.environ.get('MODE') == 'PRODUCTION':
                    web_proc = Process(target=web_main, args=(shared_conn1, child_conn))
                    web_proc.start()
                else:
                    # デバッグモードの場合、自プロセスを再起動する
                    subprocess.Popen([sys.executable, sys.argv[0]])
                    sys.exit()

            if not processing_proc.is_alive():
                logger.warning('Processing process is dead. Restarting...')
                if os.environ.get('MODE') == 'PRODUCTION':
                    processing_proc = Process(target=processing_main, args=(shared_conn2, child_conn))
                    processing_proc.start()
                else:
                    # デバッグモードの場合、自プロセスを再起動する
                    subprocess.Popen([sys.executable, sys.argv[0]])
                    sys.exit()

        except EOFError:
            pass
