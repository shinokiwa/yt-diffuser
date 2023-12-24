"""
yt_diffuser.store.store_utils のテスト
"""
import pytest

from specs.utils.test_utils.config import make_config
from specs.utils.test_utils.db import make_db

from yt_diffuser.config import AppConfig
from yt_diffuser.store import store_utils

def test_model_store_factory():
    """
    model_store_factory

    it:
        モデルストアクラスのインスタンスを生成する。
    """

    config = AppConfig()
    model_name = "test"
    revision = "test"
    class_name = "test"

    with pytest.raises(ValueError):
        store_utils.model_store_factory(config, model_name, revision, class_name)

    class_name = "ModelStore"
    assert isinstance(store_utils.model_store_factory(config, model_name, revision, class_name), store_utils.ModelStore)

    class_name = "HFModelStore"
    assert isinstance(store_utils.model_store_factory(config, model_name, revision, class_name), store_utils.HFModelStore)

def test_scan_model_dir():
    """
    scan_model_dir

    it:
        ディレクトリをスキャンし、モデルストアのリストを取得する。
    """
    config = make_config()
    conn = make_db(config)

    results = store_utils.scan_model_dir(config, conn)
    assert isinstance(results, list)
    assert len(results) == 4

    # model_name、revisionでソート
    results.sort(key=lambda x: (x.model_name, x.revision))

    r = results[0]
    assert isinstance(r, store_utils.HFModelStore)
    assert r.model_name == "test/repo_id"
    assert r.revision == "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
    assert r.commit_hash == "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
    assert r.ref == None
    assert r.screen_name == None

    r = results[1]
    assert isinstance(r, store_utils.HFModelStore)
    assert r.model_name == "test/repo_id"
    assert r.revision == "test_revision"
    assert r.commit_hash == "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    assert r.ref == "test_revision"
    assert r.screen_name == None

    r = results[2]
    assert isinstance(r, store_utils.HFModelStore)
    assert r.model_name == "test/repo_id2"
    assert r.revision == "fp16"
    assert r.commit_hash == "cccccccccccccccccccccccccccccccccccccccc"
    assert r.ref == "fp16"
    assert r.screen_name == None

    r = results[3]
    assert isinstance(r, store_utils.HFModelStore)
    assert r.model_name == "test/repo_id2"
    assert r.revision == "main"
    assert r.commit_hash == "cccccccccccccccccccccccccccccccccccccccc"
    assert r.ref == "main"
    assert r.screen_name == None