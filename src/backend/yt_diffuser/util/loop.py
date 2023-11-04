""" 無限ループ共通処理

仕組み上無限ループを使ったリスナー処理が多いのと、
完了を想定していない無限ループが多くユニットテストが難しくなるため、
無限ループ部分を共通化して、可読性とテスト容易性を高める目的のモジュール。

"""
from typing import Callable
from multiprocessing.connection import Connection
import asyncio

async def listener(conn:Connection, msg_callback:Callable, timeout:int = 1) -> bool:
    """ メッセージリスナー

    param:
        conn: Connection メッセージ受信用のコネクション
        msg_callback: Callable メッセージ受信時のasyncコールバック
        timeout: int メッセージ受信待ちのタイムアウト時間 ほぼテスト用
    """
    try:
        if conn.poll(timeout=timeout):
            msg = conn.recv()
            return not await msg_callback(msg) == False
    except (EOFError, BrokenPipeError):
        pass
    
    return True

async def loop_listener(conn:Connection = None, msg_callback:Callable = None, loop_callback:Callable = None, timeout:int = 1):
    """ メッセージ受信を開始する
    各コールバックは非同期に実行され、いずれかがFalseを返した場合はループを終了する。

    param:
        conn: Connection メッセージ受信用のコネクション
        msg_callback: Callable メッセージ受信時のasyncコールバック
        loop_callback: Callable 毎回のループで呼び出されるコールバック
        timeout: int メッセージ受信待ちのタイムアウト時間 ほぼテスト用
    """

    while True:
        tasks = []
        if conn is not None and msg_callback is not None:
            tasks.append(listener(conn, msg_callback, timeout))
        
        if loop_callback is not None:
            tasks.append(loop_callback())
        
        if len(tasks) == 0:
            return

        results = await asyncio.gather(*tasks)

        for result in results:
            if result == False:
                return
        