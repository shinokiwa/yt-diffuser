"""
yt_diffuser.utils.download.file_download のテスト
"""
import pytest
from pytest_mock import MockerFixture

from yt_diffuser.config import AppConfig
from yt_diffuser.utils.download.file_download import *

def test_hf_hub_file_download (mocker: MockerFixture):
    """
    hf_hub_file_downloadのテスト
    """
    mock_hf_hub_download = mocker.patch("yt_diffuser.utils.download.file_download.hf_hub_download", return_value="/tmp/test.txt")

    config = AppConfig(debug=True, BASE_DIR="/tmp", offline=True)

    repo_id = "yt-diffuser/yt-diffuser-test"
    filename = "model_index.json"
    revision = "main"
    filepath = hf_hub_file_download(config, repo_id, filename, revision=revision)

    assert mock_hf_hub_download.call_count == 1
    assert mock_hf_hub_download.call_args.args[0] == repo_id
    assert mock_hf_hub_download.call_args.args[1] == filename

    assert mock_hf_hub_download.call_args.kwargs["revision"] == revision

    assert filepath == "/tmp/test.txt"

    # ここからは固定値
    assert mock_hf_hub_download.call_args.kwargs["repo_type"] == REPO_TYPE_MODEL
    assert mock_hf_hub_download.call_args.kwargs["cache_dir"] == config.STORE_HF_MODEL_DIR
    assert mock_hf_hub_download.call_args.kwargs["local_files_only"] == config.offline
    assert mock_hf_hub_download.call_args.kwargs["resume_download"] == True
    assert mock_hf_hub_download.call_args.kwargs["force_download"] == False
    assert mock_hf_hub_download.call_args.kwargs["proxies"] == None
    assert mock_hf_hub_download.call_args.kwargs["local_dir_use_symlinks"] == "auto"
    assert mock_hf_hub_download.call_args.kwargs["use_auth_token"] == None
    assert mock_hf_hub_download.call_args.kwargs["subfolder"] == None