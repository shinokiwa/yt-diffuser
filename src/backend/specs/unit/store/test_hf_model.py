"""
yt_diffuser.store.hf_model のテスト
"""
import pytest

from yt_diffuser.store.hf_model import HFModelStore, AppConfig
from yt_diffuser.store.db.op.models import MODEL_CLASS_NAME

class TestHFModelStore:
    """
    HFModelStore のテスト
    """

    def test_path(self):
        """
        path プロパティ
        """
        config = AppConfig()
        store = HFModelStore(config, "test/repo_id", "test")
        assert store.path == config.STORE_HF_MODEL_DIR / "models--test--repo_id"

