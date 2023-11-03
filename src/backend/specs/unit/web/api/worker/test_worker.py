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

    def test_download (self, mocker):
        """ it: downloadはワーカープロセスに指示を出す。 """

        mock_get_shared_conn = mocker.patch('yt_diffuser.web.api.worker.get_shared_conn', return_value=mocker.Mock(send=mocker.Mock()))
        data = download()

        assert data == 'ok'
        assert mock_get_shared_conn.call_count == 1
        assert mock_get_shared_conn.return_value.send.call_count == 1