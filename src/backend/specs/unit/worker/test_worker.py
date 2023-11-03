""" worker.py のテスト
"""

from yt_diffuser.worker.worker import dispatch

class TestDispatch:
    """ describe: dispatch イベントを振り分ける """

    def test_dispatch(self, mocker):
        """ it: イベントを振り分ける """

        mock_get_shared_conn = mocker.patch('yt_diffuser.worker.worker.get_shared_conn', return_value=mocker.Mock(send=mocker.Mock()))

        dispatch("download")
        dispatch("stop_download")
        dispatch("load")
        dispatch("generate")
        dispatch("stop_generate")