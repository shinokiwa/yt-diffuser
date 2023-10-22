""" app.pyのテスト
"""
import unittest
from unittest.mock import patch

from flask import Flask

from yt_diffuser.web import app

class TestApp(unittest.TestCase):
    """app.pyのテスト
    """

    def test_app (self):
        """ appのテスト
        """
        # appのインスタンスが生成できればOK
        self.assertIsInstance(app.app, Flask)

    @unittest.skip('未実装')
    def test_send_message(self):
        """send_messageのテスト
        """

        # 戻り値は常にNone
        self.assertIsNone(app.send_message(message='test'))