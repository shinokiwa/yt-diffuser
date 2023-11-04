""" worker_listener.py のテスト """
import pytest
from unittest.mock import patch

import asyncio

from yt_diffuser.web.worker_listener import (
    get_latest_message,
    Subscriber,
    subscribe,
    unsubscribe,
    msg_callback,
    heartbeat,
    start_listener
)

class TestGetLatestMessage:
    """ describe: get_latest_message 最新のメッセージを取得する """

    def test_get_latest_message(self):
        """ it: 最新のメッセージを取得する """

        with patch("yt_diffuser.web.worker_listener._latest_messages", {'test': 'message'}):
            assert get_latest_message("test") == "message"
    
    def test_get_latest_message_no_message(self):
        """ it: メッセージがない場合はNoneを返す """

        with patch("yt_diffuser.web.worker_listener._latest_messages", {'test': 'message'}):
            assert get_latest_message("test2") == None
    
    def test_get_latest_message_other_event(self):
        """ it: 他のイベントのメッセージは取得しない """

        with patch("yt_diffuser.web.worker_listener._latest_messages", {'test': 'message', 'other': 'message'}):
            assert get_latest_message("test") == 'message'

class TestSubscriber:
    """ describe: Subscriber サブスクライバーを表すクラス """

    def test_subscriber(self):
        """ it: サブスクライバーを作成する """
        s = Subscriber()
        assert isinstance(s.queue, asyncio.Queue)
        assert isinstance(s.hb_recv, asyncio.Queue)
        assert isinstance(s.hb_send, asyncio.Queue)

    def test_heartbeat(self):
        """ it: ハートビートに対して応答する """
        s = Subscriber()
        s.hb_recv.put_nowait("hb")
        s.heartbeat()
        assert s.hb_send.get_nowait() == "hb"
    
    def test_heartbeat_timeout(self):
        """ it: ハートビートが来ていない時は何もしない """
        s = Subscriber()
        s.heartbeat()
        assert s.hb_send.empty()
    
    def test_heartbeat_other_message(self):
        """ it: ハートビート以外のメッセージが来ている時は何もしない """
        s = Subscriber()
        s.hb_recv.put_nowait("other")
        s.heartbeat()
        assert s.hb_send.empty()
    
    def test_heartbeat_full(self):
        """ it: ハートビートの応答キューは5回でいっぱいになる """
        s = Subscriber()
        s.hb_recv.put_nowait("hb")
        s.hb_recv.put_nowait("hb")
        s.hb_recv.put_nowait("hb")
        s.hb_recv.put_nowait("hb")
        assert s.hb_recv.full() == False

        s.hb_recv.put_nowait("hb")
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

class TestMsgCallback:
    """ describe: msg_callback メッセージリスナーのコールバック """

    @pytest.mark.asyncio
    async def test_default(self):
        """ it: 受信したメッセージを処理する。 """

        # Pytestでは変数パッチができないので、unittest.mock.patchを使う
        with patch("yt_diffuser.web.worker_listener._subscribers", {"test": []}) as _subscribers:

            s = Subscriber()
            _subscribers["test"].append(s)

            await msg_callback(("test", "message"))

            assert s.queue.get_nowait() == "message"

class TestHeartbeat:
    """ describe: heartbeat サブスクライバーの生存確認のため、ハートビートを送信する """

    @pytest.mark.asyncio
    async def test_heartbeat(self, mocker):
        """ it: サブスクライバーに対してハートビートを送信する """

        with patch("yt_diffuser.web.worker_listener._subscribers", {"test": []}) as _subscribers:
            s = Subscriber()
            _subscribers["test"].append(s)

            mock_unsubscribe = mocker.patch("yt_diffuser.web.worker_listener.unsubscribe")
            await heartbeat(0)

            assert s.hb_recv.get_nowait() == "hb"
            assert mock_unsubscribe.call_count == 0

    @pytest.mark.asyncio
    async def test_heartbeat_other(self, mocker):
        """ it: サブスクライバーが指定のハートビート以外を返した場合は削除する """

        with patch("yt_diffuser.web.worker_listener._subscribers", {"test": []}) as _subscribers:
            s = Subscriber()
            _subscribers["test"].append(s)

            mock_unsubscribe = mocker.patch("yt_diffuser.web.worker_listener.unsubscribe")
            s.hb_send.put_nowait("other")
            await heartbeat(0.1)

            assert mock_unsubscribe.call_count == 1
    
    @pytest.mark.asyncio
    async def test_heartbeat_full(self, mocker):
        """ it: サブスクライバーのハートビートの応答キューは5回でいっぱいになり、それでも応答がない場合は削除する """

        with patch("yt_diffuser.web.worker_listener._subscribers", {"test": []}) as _subscribers:
            s = Subscriber()
            _subscribers["test"].append(s)

            mock_unsubscribe = mocker.patch("yt_diffuser.web.worker_listener.unsubscribe")
            await heartbeat(0)
            await heartbeat(0)
            await heartbeat(0)
            await heartbeat(0)
            await heartbeat(0)

            assert mock_unsubscribe.call_count == 0

            await heartbeat(0)
            assert mock_unsubscribe.call_count == 1


class TestStartListener:
    """ describe: start_listener メッセージリスナーを起動する """

    @pytest.mark.asyncio
    async def test_start_listener(self, mocker):
        """ it: メッセージリスナーを起動する """

        mock_get_shared_conn = mocker.patch("yt_diffuser.web.worker_listener.get_shared_conn")
        mock_loop_listener = mocker.patch("yt_diffuser.web.worker_listener.loop_listener")
        mock_msg_callback = mocker.patch("yt_diffuser.web.worker_listener.msg_callback")
        mock_heartbeat = mocker.patch("yt_diffuser.web.worker_listener.heartbeat")

        tasks = await start_listener()
        await asyncio.gather(*tasks)

        assert mock_get_shared_conn.call_count == 1

        assert mock_loop_listener.call_count == 2
        assert mock_loop_listener.call_args_list[0][1]["conn"] == mock_get_shared_conn.return_value
        assert mock_loop_listener.call_args_list[0][1]["msg_callback"] == mock_msg_callback
        assert mock_loop_listener.call_args_list[1][1]["loop_callback"] == mock_heartbeat