""" yt_diffuser.utils.tqdm のテスト
"""
import pytest
import multiprocessing

from yt_diffuser.utils.tqdm import WorkerProgress

class TestWorkerProgress:
    """ 
    WorkerProgress
    """

    def test_display_spec(self, mocker):
        """
        WorkerProgress.display

        it:
            進捗を送信キューに入れる。
            キューが指定されていない場合は何もしない。
        
        test:
            トータルがゼロの時は即完了する。
            経過時間が不明の時は残り時間を不明にする。
            現在の進捗が初期値と同じ時は残り時間を不明にする。
        """

        tqdm = WorkerProgress(total=100, delay=0, mininterval=0)
        assert tqdm.update(10)

        q = multiprocessing.Queue()
        tqdm = WorkerProgress(event="test event", target="test target", total=100, delay=0, mininterval=0, queue=q)

        event, data = q.get()
        assert event == 'test event'
        assert data.keys() == {'total','target', 'progress', 'percentage', 'elapsed', 'remaining'}
        assert data['target'] == 'test target'
        assert data['total'] == 100
        assert data['progress'] == 0
        assert data['percentage'] == 0.0
        assert data['elapsed'] == 0.0
        assert data['remaining'] == -1

        tqdm.update(10)
        event, data = q.get()

        assert event == 'test event'
        assert data.keys() == {'total','target', 'progress', 'percentage', 'elapsed', 'remaining'}
        assert data['target'] == 'test target'
        assert data['progress'] == 10
        assert data['percentage'] == 10.0
        assert data['elapsed'] > 0
        assert data['remaining'] >= 0

        # トータルがゼロの時は即完了する。
        q = multiprocessing.Queue()
        tqdm = WorkerProgress(event="test event", target="test target", total=0, delay=0, mininterval=0, queue=q)

        event, data = q.get()

        assert event == 'test event'
        assert data.keys() == {'total','target', 'progress', 'percentage', 'elapsed', 'remaining'}
        assert data['target'] == 'test target'
        assert data['total'] == 0
        assert data['progress'] == 0
        assert data['percentage'] == 0.0
        assert data['elapsed'] == 0.0
        assert data['remaining'] == -1

        # 経過時間が不明の時は残り時間を不明にする。
        mock_format_dict = mocker.patch('yt_diffuser.utils.tqdm.WorkerProgress.format_dict', new_callable=mocker.PropertyMock, return_value={'elapsed': 0})
        q = multiprocessing.Queue()
        tqdm = WorkerProgress(event="test event", target="test target", total=100, delay=0, mininterval=0, queue=q)
        tqdm.display()
        event, data = q.get()

        assert tqdm.format_dict['elapsed'] == 0
        assert data['elapsed'] == 0
        assert data['remaining'] == -1

        mock_format_dict.stop()

        # 現在の進捗が初期値と同じ時は残り時間を不明にする。
        q = multiprocessing.Queue()
        tqdm = WorkerProgress(event="test event", target="test target", total=100, delay=0, mininterval=0, queue=q)
        tqdm.update(0)
        event, data = q.get()

        assert data['progress'] == 0
        assert data['percentage'] == 0.0
        assert data['remaining'] == -1
