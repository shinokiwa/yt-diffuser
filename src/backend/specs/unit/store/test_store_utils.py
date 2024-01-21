"""
yt_diffuser.store.store_utils のテスト
"""
import pytest

from specs.mock.mock_config import mock_config

from yt_diffuser.config import AppConfig
from yt_diffuser.database import connect_database
from yt_diffuser.store.store_utils import *

def test_scan_model_dir():
    """
    scan_model_dir

    it:
        ディレクトリをスキャンし、モデルストアのリストを取得する。
    """
    config = mock_config()
    conn = connect_database(":memory:")

    results = scan_model_dir(config, conn)
    assert isinstance(results, list)
    assert len(results) == 2

    # model_nameでソート
    results.sort(key=lambda x: (x.model_name))

    r = results[0]
    assert isinstance(r, ModelInfo)
    assert r.model_name == "test/repo_id"
    assert r.model_class == ModelClass.BASE_MODEL
    assert r.source == ModelSource.HUB
    assert r.screen_name == None
    assert len(r.revisions) == 2
    r.revisions.sort()
    assert r.revisions == ["bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb", "test_revision"]

    r = results[1]
    assert isinstance(r, ModelInfo)
    assert r.model_name == "test/repo_id2"
    assert r.model_class == ModelClass.BASE_MODEL
    assert r.source == ModelSource.HUB
    assert r.screen_name == None
    assert len(r.revisions) == 2
    r.revisions.sort()
    assert r.revisions == ["fp16", "main"]
