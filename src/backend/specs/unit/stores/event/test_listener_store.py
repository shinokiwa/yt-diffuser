"""
listener_store.py のテスト
"""
import pytest

from yt_diffuser.stores.event.listener_store import *

class TestEventListenerStore:
    """
    EventListenerStore のテスト
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        """
        テストの前準備
        """
        EventListenerStore._listeners = {}


    @pytest.mark.dependency()
    def test_get(self):
        """
        get メソッドのテスト
        """
        store = EventListenerStore()
        q = asyncio.Queue()
        EventListenerStore._listeners["test"] = [q]

        assert len(store.get("test")) == 1
        assert store.get("test")[0] == q
        assert store.get("test2") == []

    @pytest.mark.dependency(depends=["TestEventListenerStore::test_get"])
    def test_add(self):
        """
        add メソッドのテスト
        """
        store = EventListenerStore()
        q = asyncio.Queue()
        store.add("test", q)

        lisners = store.get("test")
        assert len(lisners) == 1
        assert lisners[0] == q

    @pytest.mark.dependency(depends=["TestEventListenerStore::test_add"])
    def test_remove(self):
        """
        remove メソッドのテスト
        """
        store = EventListenerStore()
        q = asyncio.Queue()
        store.add("test", q)
        store.remove("test", q)
        assert len(store.get("test")) == 0

