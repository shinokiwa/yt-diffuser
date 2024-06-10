"""
プロセスストアのテスト
"""
import pytest

from time import sleep

import multiprocessing

from specs.unit.injector import get_container

from yt_diffuser.stores.process.process_store import (
    ProcessStore,
    ProcessKey
)

class TestProcessStore:
    """
    プロセスストアのテスト
    """
    
    def test_create_process(self):
        """
        新規にプロセスを作成してストックする。
        同一キーが存在する場合は上書きする。
        """
        container = get_container()
        store = container.get(ProcessStore)
        process = store.create_process(ProcessKey.DOWNLOADER, lambda: None)
        assert ProcessStore._processes[ProcessKey.DOWNLOADER] == process, "プロセスがストックされている。"

        process2 = store.create_process(ProcessKey.DOWNLOADER, lambda: None)
        assert ProcessStore._processes[ProcessKey.DOWNLOADER] == process2, "プロセスが上書きされている。"
    
    def test_get_process(self):
        """
        プロセスデータを取得する。
        """
        container = get_container()
        store = container.get(ProcessStore)
        process = multiprocessing.Process()
        store.__class__._processes[ProcessKey.DOWNLOADER] = process
        assert store.get_process(ProcessKey.DOWNLOADER) == process
    
    def test_remove_process(self):
        """
        プロセスデータを削除する。
        """
        container = get_container()
        store = container.get(ProcessStore)

        def p ():
            while True:
                sleep(1)
        process = multiprocessing.Process(target=p)

        store.__class__._processes[ProcessKey.WEB] = process
        store.remove_process(ProcessKey.WEB)

        assert ProcessKey.WEB not in store.__class__._processes
        assert store.get_process(ProcessKey.WEB) == None
        assert process.is_alive() == False
    
    def test_remove_all_processes(self):
        """
        全てのプロセスデータを削除する。
        """
        container = get_container()
        store = container.get(ProcessStore)

        def p ():
            while True:
                sleep(1)
        process1 = multiprocessing.Process(target=p)
        process2 = multiprocessing.Process(target=p)
        process3 = multiprocessing.Process()

        store.__class__._processes[ProcessKey.DOWNLOADER] = process1
        store.__class__._processes[ProcessKey.GENERATOR] = process2
        store.__class__._processes[ProcessKey.WEB] = process3

        ProcessStore.remove_all_processes()

        assert store.__class__._processes == {}
        assert process1.is_alive() == False
        assert process2.is_alive() == False
        assert process3.is_alive() == False
