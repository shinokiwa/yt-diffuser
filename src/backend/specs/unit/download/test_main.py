""" yt_diffuser.download.mainのテスト
"""
import pytest
import tempfile
import multiprocessing
from pathlib import Path
import time

from huggingface_hub.hf_api import (
    ModelInfo,
    RepoFile
)

from yt_diffuser.config import AppConfig
from yt_diffuser.download.main import download_procedure
from yt_diffuser.store import connect_database

def dummy_hf_hub_download(*args, **kwargs):
    time.sleep(1)
    return str(Path(__file__).parent / "model_index.json")

def dummy_hf_api_repo_info(*args, **kwargs):
    res = ModelInfo()
    res.sha = "revision"
    res.siblings = [
        RepoFile(rfilename="scheduler/file1.txt"),
        RepoFile(rfilename="text_encoder/file2.txt"),
        RepoFile(rfilename="tokenizer/file3.txt"),
        RepoFile(rfilename="unet/file4.txt"),
    ]
    return res

def test_download_procedure_spec (mocker):
    """
    download_procedure()

    it:
        モデルファイルのダウンロードを実行する。
    """
    mock_hf_hub_download = mocker.patch('yt_diffuser.download.main.hf_hub_download',
                                        side_effect=dummy_hf_hub_download
                                        )
    mock_repo_info = mocker.patch('yt_diffuser.download.main.HfApi.repo_info', 
                                    side_effect=dummy_hf_api_repo_info
                                    )

    config = AppConfig(BASE_DIR=tempfile.mkdtemp())
    repo_id = "repo_id"
    revision = "revision"

    q = multiprocessing.Queue()
    download_procedure(
        config=config,
        queue=q,
        repo_id=repo_id,
        revision=revision
        #repo_id="CompVis/stable-diffusion-v1-4",
        #revision="fp16"
    )

    assert mock_hf_hub_download.call_count == 5

    r = q.get(timeout=5)
    assert r[0] == 'download'
    assert r[1].keys() == {'elapsed', 'percentage', 'progress', 'remaining', 'target', 'total'}
    assert r[1]['target'] == f"{repo_id}:{revision}"
    assert r[1]['total'] == 4
    assert r[1]['progress'] == 0

    download = r[1]

    # 進捗状況の受信は処理速度に依存するため、最後のもののみ確認する。
    while not q.empty():
        r = q.get(timeout=1)
        if r[0] == 'download':
            download = r[1]

    assert download['target'] == f"{repo_id}:{revision}"
    assert download['progress'] == 4
    assert download['total'] == 4

    conn = connect_database(config.DB_FILE)
    r = conn.execute("SELECT * FROM models WHERE path_name = ? AND revision = ?", (str(model.path), model.revision))
    row = r.fetchone()

    r = conn.execute("SELECT * FROM models")
    assert r.fetchall() == [(1, str(model.path), model.name, model.revision, model.class_name)]
    assert row['path_name'] == model.path
