""" loop.py のテスト
"""
import pytest
from multiprocessing import Queue
from yt_diffuser.util.loop import infinite_loop

class TestInfiniteLoop:
    """ describe: infinite_loop 無限ループ共通処理
    """

    def test_default(self):
        """ it: メッセージを受信し、コールバックを呼び出す。
        コールバックがFalseを返した場合はループを終了する。
        """
        queue = Queue()
        msg_count = 0
        loop_count = 0

        def msg_callback(msg):
            nonlocal msg_count
            msg_count += 1

            if msg == "exit":
                return False

        def loop_callback():
            nonlocal loop_count
            loop_count += 1

            return loop_count < 3

        queue.put("exit")
        infinite_loop(queue=queue, msg_callback=msg_callback, loop_callback=loop_callback, timeout=0.1)

        assert msg_count == 1
        assert loop_count == 0

        msg_count = 0
        loop_count = 0

        queue.put("test")
        queue.put("test")
        queue.put("test")
        infinite_loop(queue=queue, msg_callback=msg_callback, loop_callback=loop_callback, timeout=0.1)

        assert msg_count == 3
        assert loop_count == 3

    def test_only_callback(self):
        """ it: メッセージコールバックのみ、ループコールバックのみでも動作する。
        """
        queue = Queue()
        msg_count = 0
        loop_count = 0

        def msg_callback(msg):
            nonlocal msg_count
            msg_count += 1

            return False

        def loop_callback():
            nonlocal loop_count
            loop_count += 1

            return False

        queue.put("test")
        infinite_loop(queue=queue, msg_callback=msg_callback, timeout=0.1)

        assert msg_count == 1
        assert loop_count == 0

        msg_count = 0
        loop_count = 0
        infinite_loop(loop_callback=loop_callback, timeout=0.1)

        assert msg_count == 0
        assert loop_count == 1