"""
プロセスコンテキストストアのテスト
"""
import pytest

from yt_diffuser.stores.process.process_context_store import (
    ProcessContextStore,
    SpawnContext,
)

class TestProcessContextStore:
    """
    プロセスコンテキストストアのテスト
    """
    
    def test_get_context(self):
        """
        プロセスコンテキストを取得する。
        """
        store = ProcessContextStore()
        context = store.get_context()
        assert isinstance(context, SpawnContext)
        assert context == store.__class__._context
    