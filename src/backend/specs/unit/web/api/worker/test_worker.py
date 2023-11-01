""" worker のテスト
"""
from flask import Blueprint

from yt_diffuser.web.api.worker import worker_bp, download

class TestWorkerBp:
    """ describe: worker_bp Blueprintオブジェクト"""

    def test_worker_bp(self):
        """ it: worker_bpはBlueprintオブジェクト """

        assert type(worker_bp) == Blueprint

class TestDownload:
    """ describe: download ワーカープロセスに指示を出す """

    def test_download (self):
        """ it: downloadはワーカープロセスに指示を出す。 """

        data = download()

        assert data == 'ok'