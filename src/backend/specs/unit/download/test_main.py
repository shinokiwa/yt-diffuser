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
from u_dam.sqlite3 import setup_database

from yt_diffuser.config import AppConfig
from yt_diffuser.database import connect_database
from yt_diffuser.download.main import download_procedure

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
    #setup_database(config.DB_FILE, config.DB_UPDATE_FILE, config.DB_VERSION)
    (config.STORE_HF_MODEL_DIR / "models--repo_id").mkdir(parents=True, exist_ok=True)
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

    message = []
    download = []
    while not q.empty():
        r = q.get(timeout=1)
        if r[0] == 'download':
            download.append(r)
        elif r[0] == 'message':
            message.append(r)

    assert len(message) == 2
    assert message[0][1].keys() == {'label', 'target'}
    assert message[0][1]['label'] == 'download-start'
    assert message[0][1]['target'] == f"{repo_id}:{revision}"
    assert message[1][1].keys() == {'label', 'target'}
    assert message[1][1]['label'] == 'download-complete'
    assert message[1][1]['target'] == f"{repo_id}:{revision}"

    assert download[0][0] == 'download'
    assert download[0][1].keys() == {'elapsed', 'percentage', 'progress', 'remaining', 'target', 'total'}
    assert download[0][1]['target'] == f"{repo_id}:{revision}"
    assert download[0][1]['progress'] == 0
    assert download[0][1]['total'] == 4

    assert download[-1][1]['target'] == f"{repo_id}:{revision}"
    assert download[-1][1]['progress'] == 4
    assert download[-1][1]['total'] == 4
