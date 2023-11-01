""" ワーカープロセスからのメッセージを受け取るモジュール
Pub-Subパターンで実装する。
"""
from logging import getLogger; logger = getLogger(__name__)
import gevent
from gevent.queue import Queue, Empty

from yt_diffuser.web.connection import get_shared_conn

_subscribers = {}
_latest_messages = {}

class Subscriber:
    """ サブスクライバーを表すクラス
    """

    def __init__(self):
        self.queue = Queue()
        self.hb_recv = Queue(maxsize=5)
        self.hb_send = Queue()
    
    def heartbeat(self):
        """ ハートビートに対して応答する
        """
        if self.hb_recv.empty():
            return

        msg = self.hb_recv.get_nowait()
        if msg == "hb":
            self.hb_send.put("hb")

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

def start_listener():
    """ メッセージ受信を開始する
    """
    worker_conn = get_shared_conn()
    logger.debug("Start worker listener")

    while True:
        try:
            if worker_conn.closed:
                gevent.sleep(1)
                continue

            if worker_conn.poll(timeout=1):
                (event, data) = worker_conn.recv()
                _latest_messages[event] = data

                for subscriber in _subscribers.get(event, []):
                    subscriber.queue.put(data)

        except EOFError:
            pass

        gevent.sleep(0)

def start_heartbeat():
    """ サブスクライバーの生存確認のため、ハートビートを送信する
    サブスクライバーは"hb"の文字列を受信したら、"hb"を返すことで生存確認を行う。
    生存確認が取れない場合は、サブスクライバーを削除する。
    """
    logger.debug("Start worker listener heartbeat checker")
    while True:
        for event in _subscribers.keys():
            # unsubscribeされる可能性があるので、コピーを作成する
            subscribers = _subscribers[event]

            for subscriber in subscribers:
                try:
                    # キューが満杯の場合失敗とみなし、サブスクライバーを削除する
                    if subscriber.hb_recv.full():
                        unsubscribe(event, subscriber)
                        continue

                    subscriber.hb_recv.put("hb")

                    msg = subscriber.hb_send.get(timeout=1)
                    if msg != "hb":
                        unsubscribe(event, subscriber)

                except Empty:
                    pass

        gevent.sleep(10)

def start_greenlets ():
    """ Greenletを起動する
    """
    logger.debug("Start worker listener greenlets")

    listener = gevent.spawn(start_listener)
    listener.start()

    heartbeat_checker = gevent.spawn(start_heartbeat)
    heartbeat_checker.start()