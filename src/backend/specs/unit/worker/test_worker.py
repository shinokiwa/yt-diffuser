""" worker.py のテスト
"""

from yt_diffuser.worker.worker import dispatch

class TestDispatch:
    """ describe: dispatch イベントを振り分ける """

    def test_dispatch(self, mocker):
        """ it: イベントを振り分ける """

        dispatch("download")
        dispatch("stop_download")
        dispatch("load")
        dispatch("generate")
        dispatch("stop_generate")