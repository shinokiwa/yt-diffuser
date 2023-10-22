""" sseのテスト
"""
import unittest

from flask import Blueprint, Response
import json

from yt_diffuser.web.api.sse import sse_bp, status_stream, get_status

class TestSse(unittest.TestCase):
    """sseのテスト
    """

    def test_sse_bp (self):
        """ sse_bpのテスト
        """
        # sse_bpのインスタンスが生成できればOK
        self.assertIsInstance(sse_bp, Blueprint)

    def test_status_stream (self):
        """ status_streamのテスト
        """

        # status_streamの戻り値はgenerator
        res = next(status_stream())

        # yieldで返すデータの型はstr
        self.assertIsInstance(res, str)
        self.assertRegex(res, r'data: {".+"}\n\n')

        res_dict = json.loads(res[6:-2])

        self.assertIn('status', res_dict.keys())
        self.assertRegex(res_dict['status'], r'\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}')

    def test_get_status (self):
        """ get_statusのテスト
        """
        # 戻り値はResponse
        res = get_status()
        self.assertIsInstance(res, Response)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.mimetype, 'text/event-stream')
        
        # Responseのdataはstr
        data = next(res.response)
        self.assertIsInstance(data, str)
        self.assertRegex(data, r'data: {".+"}\n\n')

        res_dict = json.loads(data[6:-2])

        # 内容はstatus_streamの戻り値と同じ
        self.assertIn('status', res_dict.keys())


if __name__ == '__main__':
    unittest.main()