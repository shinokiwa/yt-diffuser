""" main.pyのテスト
"""
import os
import unittest
from unittest.mock import patch

from yt_diffuser.web.main import web_procedure

class TestMain(unittest.TestCase):
    """main.pyのテスト
    """

    @patch.dict(os.environ, {"MODE": "DEBUG"})
    @patch("yt_diffuser.web.main.WSGIServer.serve_forever")
    @patch("yt_diffuser.web.main.app.app.run")
    def test_web_procedure_debug(self, mock_run, mock_server):
        """web_procedureのテスト
        DEBUGモードの場合
        """

        # 現状は該当モジュールが暫定なのでテストも暫定

        # 戻り値は常にNone
        self.assertIsNone(web_procedure(shared_conn=None, parent_conn=None))

        # WSGIServerは呼ばれない
        mock_server.assert_not_called()

        # runは呼ばれる
        mock_run.assert_called_once_with(host='0.0.0.0', port=8000, debug=True)
    
    @patch.dict(os.environ, {"MODE": "PRODUCTION"})
    @patch("yt_diffuser.web.main.WSGIServer.serve_forever")
    @patch("yt_diffuser.web.main.app.app.run")
    def test_web_procedure_production(self, mock_run, mock_server):
        """web_procedureのテスト
        PRODUCTIONモードの場合
        """

        # 現状は該当モジュールが暫定なのでテストも暫定

        # 戻り値は常にNone
        self.assertIsNone(web_procedure(shared_conn=None, parent_conn=None))

        # runは呼ばれない
        mock_run.assert_not_called()

        # WSGIServerは呼ばれる
        mock_server.assert_called_once()
    
