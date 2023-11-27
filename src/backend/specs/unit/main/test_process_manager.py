""" process_manager.pyのテスト """
import pytest
from unittest.mock import patch
import time

import multiprocessing
from multiprocessing.queues import Queue
from multiprocessing.context import SpawnProcess

from yt_diffuser.main import process_manager

@pytest.mark.describe("stop_all")
@pytest.mark.it("登録されている全プロセスを終了し、クリーンアップする。")    
def test_stop_all_spec(mocker):

    web_procedure = mocker.patch('yt_diffuser.main.process_manager.web_procedure', dummy_proc_loop)
    worker_procedure = mocker.patch('yt_diffuser.main.process_manager.worker_procedure', dummy_proc_loop)

    process_manager.web_send_queue = multiprocessing.Queue
    process_manager.worker_send_queue = multiprocessing.Queue()

    process_manager.web_process = multiprocessing.Process(target=web_procedure, args=[process_manager.web_send_queue, process_manager.worker_send_queue])
    process_manager.worker_process = multiprocessing.Process(target=worker_procedure, args=[process_manager.worker_send_queue, process_manager.web_send_queue])
    process_manager.web_process.start()
    process_manager.worker_process.start()

    process_manager.stop_all()
    
    assert process_manager.web_process is None
    assert process_manager.worker_process is None
    assert process_manager.web_send_queue is None
    assert process_manager.worker_send_queue is None

@pytest.mark.it("プロセスが動いていないときに実行しても何も起きない。")    
def test_stop_all_no_process(mocker):

    web_procedure = mocker.patch('yt_diffuser.main.process_manager.web_procedure')
    worker_procedure = mocker.patch('yt_diffuser.main.process_manager.worker_procedure')

    process_manager.web_send_queue = multiprocessing.Queue
    process_manager.worker_send_queue = multiprocessing.Queue()

    process_manager.web_process = None
    process_manager.worker_process = None

    process_manager.stop_all()
    
    assert process_manager.web_process is None
    assert process_manager.worker_process is None
    assert process_manager.web_send_queue is None
    assert process_manager.worker_send_queue is None

    process_manager.web_process = multiprocessing.Process(target=web_procedure, args=[process_manager.web_send_queue, process_manager.worker_send_queue])
    process_manager.worker_process = multiprocessing.Process(target=worker_procedure, args=[process_manager.worker_send_queue, process_manager.web_send_queue])

    process_manager.stop_all()

    assert process_manager.web_process is None
    assert process_manager.worker_process is None
    assert process_manager.web_send_queue is None
    assert process_manager.worker_send_queue is None


class TestSignalHandler:
    """ describe: signal_handler 終了シグナルハンドラ """

    def test_signal_handler(self):
        """ it: 終了シグナルを受け取った場合にstop_allを呼び出し、プロセスを終了する。基本的にsignal.signalで登録して使う。 
        """

        with patch('yt_diffuser.main.process_manager.stop_all') as mock_stop_all:

            with pytest.raises(SystemExit):
                process_manager.signal_handler(0, None)

        mock_stop_all.assert_called_once()

@pytest.mark.describe("start_processes")
@pytest.mark.it("サブプロセスを初期化する。終了時にはstop_allが呼ばれる。")
def test_start_process_spec (mocker):

    web_procedure = mocker.patch('yt_diffuser.main.process_manager.web_procedure', dummy_proc_loop)
    worker_procedure = mocker.patch('yt_diffuser.main.process_manager.worker_procedure', dummy_proc_loop)

    process_manager.start_processes()

    assert type(process_manager.web_send_queue) == Queue
    assert type(process_manager.worker_send_queue) == Queue

    assert type(process_manager.web_process) == SpawnProcess
    assert process_manager.web_process.is_alive() == True

    assert type(process_manager.worker_process) == SpawnProcess
    assert process_manager.worker_process.is_alive() == True

    process_manager.web_process.terminate()
    process_manager.web_process.join()
    process_manager.worker_process.terminate()
    process_manager.worker_process.join()

@pytest.mark.it("サブプロセス同士はQueueを使って通信できる。送信用、受信用それぞれで渡される。")
def test_queue(mocker):
    web_procedure = mocker.patch('yt_diffuser.main.process_manager.web_procedure', dummy_proc_send)
    worker_procedure = mocker.patch('yt_diffuser.main.process_manager.worker_procedure', dummy_proc_recv)

    process_manager.start_processes()

    assert process_manager.worker_send_queue.get(timeout=5) == "dummy reply"

    web_procedure = mocker.patch('yt_diffuser.main.process_manager.web_procedure', dummy_proc_recv)
    worker_procedure = mocker.patch('yt_diffuser.main.process_manager.worker_procedure', dummy_proc_send)

    process_manager.start_processes()

    assert process_manager.web_send_queue.get(timeout=5) == "dummy reply"

class TestCheckProcesses:
    """ describe: check_processes プロセス監視 """

    def test_default (self, mocker):
        """ it: プロセスが停止していた場合、再起動する。
        停止していない場合は何もしない。
        """

        web_procedure = mocker.patch('yt_diffuser.main.process_manager.web_procedure', dummy_proc_loop)
        worker_procedure = mocker.patch('yt_diffuser.main.process_manager.worker_procedure', dummy_proc_loop)

        process_manager.check_processes()

        assert type(process_manager.web_process) == SpawnProcess
        assert process_manager.web_process.is_alive() == True
        assert type(process_manager.worker_process) == SpawnProcess
        assert process_manager.worker_process.is_alive() == True
 
        process_manager.web_process.terminate()
        process_manager.web_process.join()
        process_manager.worker_process.terminate()
        process_manager.worker_process.join()

        process_manager.check_processes()

        assert type(process_manager.web_process) == SpawnProcess
        assert process_manager.web_process.is_alive() == True
        assert type(process_manager.worker_process) == SpawnProcess
        assert process_manager.worker_process.is_alive() == True
 
        process_manager.web_process.terminate()
        process_manager.web_process.join()
        process_manager.worker_process.terminate()
        process_manager.worker_process.join()

@pytest.mark.describe("start_loop")
@pytest.mark.it("サブプロセスが起動され、監視が開始される。")
def test_start_all(mocker):

    mock_atexit_unregister = mocker.patch('yt_diffuser.main.process_manager.atexit.unregister')
    mock_atexit_register = mocker.patch('yt_diffuser.main.process_manager.atexit.register')
    mock_signal = mocker.patch('yt_diffuser.main.process_manager.signal.signal')
    mock_start_processes = mocker.patch('yt_diffuser.main.process_manager.start_processes')
    mock_check_processes = mocker.patch('yt_diffuser.main.process_manager.check_processes')
    mock_infinite_loop = mocker.patch('yt_diffuser.main.process_manager.infinite_loop')
    mock_stop_all = mocker.patch('yt_diffuser.main.process_manager.stop_all')

    process_manager.start_loop()

    assert mock_atexit_unregister.call_count == 1
    assert mock_atexit_register.call_count == 1
    assert mock_signal.call_count == 2
    assert mock_start_processes.call_count == 1
    assert mock_infinite_loop.call_count == 1
    assert mock_infinite_loop.call_args[1]["loop_callback"] == mock_check_processes
    assert mock_stop_all.call_count == 1

@pytest.mark.it("KeyboardInterruptを受け取った場合にstop_allを呼び出し、プロセスを終了する。")
def test_start_loop_interrupt (mocker):

    mock_atexit_unregister = mocker.patch('yt_diffuser.main.process_manager.atexit.unregister')
    mock_atexit_register = mocker.patch('yt_diffuser.main.process_manager.atexit.register')
    mock_signal = mocker.patch('yt_diffuser.main.process_manager.signal.signal')
    mock_start_processes = mocker.patch('yt_diffuser.main.process_manager.start_processes')
    mock_check_processes = mocker.patch('yt_diffuser.main.process_manager.check_processes')
    mock_infinite_loop = mocker.patch('yt_diffuser.main.process_manager.infinite_loop', side_effect=KeyboardInterrupt)
    mock_stop_all = mocker.patch('yt_diffuser.main.process_manager.stop_all')

    process_manager.start_loop()

    assert mock_atexit_unregister.call_count == 1
    assert mock_atexit_register.call_count == 1
    assert mock_signal.call_count == 2
    assert mock_start_processes.call_count == 1
    assert mock_infinite_loop.call_count == 1
    assert mock_infinite_loop.call_args[1]["loop_callback"] == mock_check_processes
    assert mock_stop_all.call_count == 1



def dummy_proc(send_queue:Queue, recv_queue:Queue):
    """ ダミープロシージャ 即終了
    """
    return

def dummy_proc_loop(send_queue:Queue, recv_queue:Queue):
    """ ダミープロシージャ 無限ループ
    """
    while True:
        time.sleep(1)

def dummy_proc_send(send_queue:Queue, recv_queue:Queue):
    """ ダミープロシージャ メッセージ送信
    """
    send_queue.put("dummy")

def dummy_proc_recv(send_queue:Queue, recv_queue:Queue):
    """ ダミープロシージャ メッセージ受信
    """
    msg = recv_queue.get()
    if msg == "dummy":
        send_queue.put("dummy reply")