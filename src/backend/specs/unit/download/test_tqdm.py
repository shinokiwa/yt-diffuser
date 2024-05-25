""" yt_diffuser.utils.tqdm のテスト
"""
import pytest
from pytest_mock import MockerFixture
import multiprocessing

from yt_diffuser.utils.event import DownloadStatusEvent
from yt_diffuser.download.tqdm import *

class TestDownloadProgress:
    """ 
    DownloadProgress
    """

    def test_display_spec(self, mocker: MockerFixture):
        """
        DownloadProgress.display

        it:
            進捗を送信キューに入れる。
            キューが指定されていない場合は何もしない。
        
        test:
            トータルがゼロの時は即完了する。
            経過時間が不明の時は残り時間を不明にする。
            現在の進捗が初期値と同じ時は残り時間を不明にする。
        """

        tqdm = DownloadProgress(total=100, delay=0, mininterval=0)
        assert tqdm.update(10)

        q = multiprocessing.Queue()
        tqdm = DownloadProgress(
            model_name="test model",
            revision="test revision",
            total=100,
            delay=0,
            mininterval=0,
            queue=q
        )

        event, cache, data = q.get()
        assert event == DownloadStatusEvent.event_name
        assert cache == DownloadStatusEvent.cache

        assert data.keys() == {'status', 'model_name', 'revision', 'total', 'progress', 'percentage', 'elapsed', 'remaining', 'error'}
        assert data['status'] == DownloadStatusEvent.Status.DOWNLOADING.value
        assert data['model_name'] == "test model"
        assert data['revision'] == "test revision"
        assert data['total'] == 100
        assert data['progress'] == 0
        assert data['percentage'] == 0.0
        assert data['elapsed'] == 0.0
        assert data['remaining'] == -1

        tqdm.update(10)
        event, cache, data = q.get()

        assert data.keys() == {'status', 'model_name', 'revision', 'total', 'progress', 'percentage', 'elapsed', 'remaining', 'error'}
        assert data['status'] == DownloadStatusEvent.Status.DOWNLOADING.value
        assert data['model_name'] == "test model"
        assert data['revision'] == "test revision"
        assert data['total'] == 100
        assert data['progress'] == 10
        assert data['percentage'] == 10.0
        assert data['elapsed'] > 0
        assert data['remaining'] >= 0

        # トータルがゼロの時は即完了する。
        q = multiprocessing.Queue()
        tqdm = DownloadProgress(
            model_name="test model",
            revision="test revision",
            total=0,
            delay=0,
            mininterval=0,
            queue=q
        )

        event, cache, data = q.get()

        assert data['total'] == 0
        assert data['progress'] == 0
        assert data['percentage'] == 0.0
        assert data['elapsed'] == 0.0
        assert data['remaining'] == -1


        # 経過時間が不明の時は残り時間を不明にする。
        mock_format_dict = mocker.patch('yt_diffuser.download.tqdm.DownloadProgress.format_dict', new_callable=mocker.PropertyMock, return_value={'elapsed': 0})
        q = multiprocessing.Queue()
        tqdm = DownloadProgress(
            model_name="test model",
            revision="test revision",
            total=100,
            delay=0,
            mininterval=0,
            queue=q
        )
        tqdm.display()
        event, cache, data = q.get()

        assert tqdm.format_dict['elapsed'] == 0
        assert data['elapsed'] == 0
        assert data['remaining'] == -1

        mock_format_dict.stop()

        # 現在の進捗が初期値と同じ時は残り時間を不明にする。
        q = multiprocessing.Queue()
        tqdm = DownloadProgress(
            model_name="test model",
            revision="test revision",
            total=100,
            delay=0,
            mininterval=0,
            queue=q
        )
        tqdm.update(0)
        event, cache, data = q.get()

        assert data['progress'] == 0
        assert data['percentage'] == 0.0
        assert data['remaining'] == -1
