""" 無限ループ共通処理

仕組み上無限ループを使ったリスナー処理が多いのと、
完了を想定していない無限ループが多くユニットテストが難しくなるため、
無限ループ部分を共通化して、可読性とテスト容易性を高める目的のモジュール。

"""
from typing import Callable
import multiprocessing
from multiprocessing.queues import Queue
from queue import Empty
import time

def infinite_loop(queue:Queue = None, msg_callback:Callable = None, loop_callback:Callable = None, timeout:float = 1.0):
    """ メッセージ受信を開始する
    各コールバックは非同期に実行され、いずれかがFalseを返した場合はループを終了する。

    param:
        queue: Queue メッセージ受信用のコネクション
        msg_callback: Callable メッセージ受信時のasyncコールバック
        loop_callback: Callable 毎回のループで呼び出されるコールバック
        timeout: int メッセージ受信待ちのタイムアウト時間 ほぼテスト用
    """

    while True:
        if queue is not None and msg_callback is not None:
            try:
                msg = queue.get(timeout=timeout)
                if msg_callback(msg) == False:
                    return
            except Empty:
                pass
        else:
            time.sleep(timeout)
        
        if loop_callback is not None:
            if loop_callback() == False:
                return
        