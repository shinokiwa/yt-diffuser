""" ワーカープロセスからのメッセージを受け取るモジュール
Pub-Subパターンで実装する。
"""
from logging import getLogger; logger = getLogger(__name__)
import asyncio
from asyncio import Queue

from yt_diffuser.web.connection import get_shared_conn
from yt_diffuser.util.loop import loop_listener

_subscribers = {}
_latest_messages = {}

class Subscriber:
    """ サブスクライバーを表すクラス
    """

    def __init__(self, receiver):
        self.receiver = receiver
        self.hb_recv = Queue(maxsize=5)
        self.hb_send = Queue()
    
    def heartbeat(self):
        """ ハートビートに対して応答する
        """
        if self.hb_recv.empty():
            return

        msg = self.hb_recv.get_nowait()
        if msg == "hb":
            self.hb_send.put_nowait("hb")

def get_latest_message(event):
    """ 最後のメッセージを取得する
    """
    return _latest_messages.get(event, None)

def subscribe(event, subscriber:Subscriber):
    """ イベントに対してキューを登録する
    """
    if event not in _subscribers:
        _subscribers[event] = []

    logger.debug(f"subscribe: {event}")
    _subscribers[event].append(subscriber)

def unsubscribe(event, subscriber:Subscriber):
    """ イベントに対して登録されているコールバックを削除する
    """
    if event not in _subscribers:
        return
    
    logger.debug(f"unsubscribe: {event}")
    if subscriber in _subscribers[event]:
        _subscribers[event].remove(subscriber)

async def msg_callback(msg):
    """ メッセージ受信コールバック
    """
    (event, data) = msg
    _latest_messages[event] = data

    for subscriber in _subscribers.get(event, []):
        subscriber.receiver(data)


async def heartbeat(timeout:float=10.0):
    """ サブスクライバーの生存確認のため、ハートビートを送信する
    サブスクライバーは"hb"の文字列を受信したら、"hb"を返すことで生存確認を行う。
    生存確認が取れない場合は、サブスクライバーを削除する。

    param:
        timeout: float ハートビートのタイムアウト時間 ほぼテスト用
    """

    # 非同期にunsubscribeされる可能性があるので、コピーを作成する
    subscribers = _subscribers

    for event in subscribers.keys():
        for subscriber in subscribers[event]:

            # キューが満杯の場合失敗とみなし、サブスクライバーを削除する
            if subscriber.hb_recv.full():
                unsubscribe(event, subscriber)
                continue

            subscriber.hb_recv.put_nowait("hb")

            try:
                msg = await asyncio.wait_for(subscriber.hb_send.get(), timeout=timeout)
                if msg != "hb":
                    unsubscribe(event, subscriber)

            except asyncio.TimeoutError:
                pass

async def start_listener ()->[]:
    """ リスナーを起動する
    """
    logger.debug("Start worker listener greenlets")

    conn = get_shared_conn()

    tasks = [
        asyncio.create_task(loop_listener(conn=conn, msg_callback=msg_callback)),
        asyncio.create_task(loop_listener(loop_callback=heartbeat))
    ]

    return tasks