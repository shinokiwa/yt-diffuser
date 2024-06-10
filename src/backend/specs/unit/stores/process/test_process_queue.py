"""
プロセスストアのテスト
"""
import multiprocessing.queues
import pytest

import multiprocessing

from specs.unit.injector import get_container

from yt_diffuser.stores.process.process_queue_store import (
    ProcessQueueStore,
    ProcessKey
)

class TestProcessQueueStore:
    """
    プロセスキューストアのテスト
    """

    @pytest.mark.dependency()
    def test_create_queue(self):
        """
        新規にキューを作成してストックする。
        同一キーが存在する場合は上書きする。
        """
        container = get_container()
        store = container.get(ProcessQueueStore)
        queue = store.create_queue(ProcessKey.DOWNLOADER)

        assert isinstance(queue, multiprocessing.queues.Queue)
        assert store.__class__._queues[ProcessKey.DOWNLOADER] == queue
    
    @pytest.mark.dependency(depends=["TestProcessQueueStore::test_create_queue"])
    def test_get_queue(self):
        """
        キューを取得する。
        存在しない場合はNoneを返す。
        """
        container = get_container()
        store = container.get(ProcessQueueStore)
        queue = store.get_queue(ProcessKey.GENERATOR)
        assert store.get_queue(ProcessKey.GENERATOR) == queue

        store.__class__._queues = {}

        assert store.get_queue(ProcessKey.GENERATOR) == None
    
    @pytest.mark.dependency(depends=["TestProcessQueueStore::test_create_queue"])
    def test_get_self_queue(self):
        """
        自分自身のキューを取得する。
        存在しない場合は新規に作成する。
        """
        container = get_container()
        store = container.get(ProcessQueueStore)
        queue = store.get_self_queue()
        assert isinstance(queue, multiprocessing.queues.Queue)
        assert store.__class__._queues[ProcessKey.SELF] == queue
    
    @pytest.mark.dependency(depends=["TestProcessQueueStore::test_create_queue"])
    def test_remove_queue(self):
        """
        キューを削除する。
        """
        container = get_container()
        store = container.get(ProcessQueueStore)
        store.remove_queue(ProcessKey.DOWNLOADER)

        assert store.get_queue(ProcessKey.DOWNLOADER) == None
   