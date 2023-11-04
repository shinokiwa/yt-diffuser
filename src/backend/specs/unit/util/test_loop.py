""" loop.py のテスト
"""
import pytest
import asyncio
from multiprocessing import Pipe
from yt_diffuser.util.loop import listener, loop_listener

class TestListener:
    """ describe: listener メッセージリスナー
    """

    @pytest.mark.asyncio
    async def test_default(self, mocker):
        """ it: メッセージを受信し、コールバックを呼び出す。
        コールバックがFalseを返した場合はFalseを返す。それ以外はTrueを返す。
        """
        parent_conn, child_conn = Pipe()

        msg_callback = mocker.AsyncMock()
        parent_conn.send("test")
        assert await listener(conn=child_conn, msg_callback=msg_callback) == True

        assert msg_callback.call_count == 1
        assert msg_callback.call_args[0][0] == "test"

        msg_callback.return_value = True
        parent_conn.send("test")
        assert await listener(conn=child_conn, msg_callback=msg_callback) == True

        msg_callback.return_value = False
        parent_conn.send("test")
        assert await listener(conn=child_conn, msg_callback=msg_callback) == False

    @pytest.mark.asyncio
    async def test_no_message(self, mocker):
        """ it: メッセージがない場合は何もしない
        """

        receiver = mocker.AsyncMock(return_value=True)
        parent_conn, child_conn = Pipe()

        assert await listener(conn=child_conn, msg_callback=receiver, timeout=0) == True
        assert receiver.call_count == 0

class TestLoopListener:
    """ describe: loop_listner 無限ループ共通処理
    """

    @pytest.mark.asyncio
    async def test_default(self, mocker):
        """ it: 無限ループでメッセージを受信する。
        コールバックがFalseを返した場合はループを終了する。
        """
        parent_conn, child_conn = Pipe()
        listener_mock = mocker.patch('yt_diffuser.util.loop.listener')
        msg_callback = mocker.AsyncMock()
        loop_count = 0

        async def loop_callback():
            nonlocal loop_count
            loop_count += 1

            return loop_count < 3

        assert await loop_listener(conn=child_conn, msg_callback=msg_callback, loop_callback=loop_callback, timeout=0) == None

        assert listener_mock.call_count == 3
        assert listener_mock.call_args[0][0] == child_conn
        assert listener_mock.call_args[0][1] == msg_callback
        assert loop_count == 3

    @pytest.mark.asyncio
    async def test_only_callback(self, mocker):
        """ it: メッセージコールバックのみ、ループコールバックのみでも動作する。
        """
        parent_conn, child_conn = Pipe()
        listener_mock = mocker.patch('yt_diffuser.util.loop.listener', return_value=False)
        msg_callback = mocker.AsyncMock()

        loop_count = 0
        async def loop_callback():
            nonlocal loop_count
            loop_count += 1
            return loop_count < 3

        # メッセージコールバックのみ
        assert await loop_listener(conn=child_conn, msg_callback=msg_callback, timeout=0) == None

        assert listener_mock.call_count == 1
        assert listener_mock.call_args[0][0] == child_conn
        assert listener_mock.call_args[0][1] == msg_callback
        assert loop_count == 0

        # ループコールバックのみ
        loop_count = 0
        listener_mock.reset_mock()
        listener_mock.return_value = True

        assert await loop_listener(loop_callback=loop_callback, timeout=0) == None

        assert listener_mock.call_count == 0
        assert loop_count == 3

    @pytest.mark.asyncio
    async def test_no_args(self, mocker):
        """ it: 引数がない場合は何もしない。ループもしない。
        """
        assert await loop_listener() is None