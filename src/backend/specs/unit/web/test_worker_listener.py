""" worker_listener.py のテスト """
import pytest
from unittest.mock import patch

from multiprocessing import Pipe
from multiprocessing.connection import Connection
import gevent
from gevent.queue import Queue, Full

from yt_diffuser.web.worker_listener import (
    Subscriber,
    subscribe,
    unsubscribe,
    start_listener
)

class TestSubscriber:
    """ describe: Subscriber サブスクライバーを表すクラス """

    def test_subscriber(self):
        """ it: サブスクライバーを作成する """
        s = Subscriber()
        assert isinstance(s.queue, Queue)
        assert isinstance(s.hb_recv, Queue)
        assert isinstance(s.hb_send, Queue)

    def test_heartbeat(self):
        """ it: ハートビートに対して応答する """
        s = Subscriber()
        s.hb_recv.put("hb")
        s.heartbeat()
        assert s.hb_send.get() == "hb"
    
    def test_heartbeat_timeout(self):
        """ it: ハートビートが来ていない時は何もしない """
        s = Subscriber()
        s.heartbeat()
        assert s.hb_send.empty()
    
    def test_heartbeat_other_message(self):
        """ it: ハートビート以外のメッセージが来ている時は何もしない """
        s = Subscriber()
        s.hb_recv.put("other")
        s.heartbeat()
        assert s.hb_send.empty()
    
    def test_heartbeat_full(self):
        """ it: ハートビートの応答キューは5回でいっぱいになる """
        s = Subscriber()
        s.hb_recv.put("hb")
        s.hb_recv.put("hb")
        s.hb_recv.put("hb")
        s.hb_recv.put("hb")
        assert s.hb_recv.full() == False

        s.hb_recv.put("hb")
        assert s.hb_recv.full() == True

class TestSubscribe:
    """ describe: subscribe イベントに対してキューを登録する """

    def test_subscribe(self):
        """ it: イベントに対してキューを登録する """

        with patch("yt_diffuser.web.worker_listener._subscribers", {}) as _subscribers:
            s = Subscriber()
            subscribe("test", s)
            assert _subscribers["test"][0] == s

class TestUnsubscribe:
    """ describe: unsubscribe イベントに対して登録されているコールバックを削除する """

    def test_unsubscribe(self):
        """ it: イベントに対して登録されているコールバックを削除する """

        with patch("yt_diffuser.web.worker_listener._subscribers", {"test": []}) as _subscribers:
            s = Subscriber()
            _subscribers["test"].append(s)
            unsubscribe("test", s)
            assert len(_subscribers["test"]) == 0

    def test_unsubscribe_other_event(self):
        """ it: 他のイベントのコールバックは削除しない """

        with patch("yt_diffuser.web.worker_listener._subscribers", {"test": [], "other": []}) as _subscribers:
            s = Subscriber()
            _subscribers["test"].append(s)
            unsubscribe("other", s)
            assert len(_subscribers["test"]) == 1

    def test_unsubscribe_no_event(self):
        """ it: イベントが存在しない場合は何もしない """

        with patch("yt_diffuser.web.worker_listener._subscribers", {}) as _subscribers:
            s = Subscriber()
            unsubscribe("test", s)
            assert len(_subscribers) == 0

class TestStartListener:
    """ describe: start_listener メッセージ受信を開始する """

    def test_start_listener(self):
        """ it: メッセージ受信を開始する。 """
        with patch("yt_diffuser.web.worker_listener.get_shared_conn") as get_shared_conn, \
            patch("yt_diffuser.web.worker_listener._subscribers", {"test": []}) as _subscribers:
            parent_conn, child_conn = Pipe()
            get_shared_conn.return_value = child_conn

            s = Subscriber()
            _subscribers["test"].append(s)

            gl = gevent.spawn(start_listener)
            gl.start()
            gevent.sleep(0)
            assert get_shared_conn.call_count == 1

            parent_conn.send(("test", "message"))
            gevent.sleep(0)
            assert s.queue.get(timeout=5) == "message"

            gl.kill()
