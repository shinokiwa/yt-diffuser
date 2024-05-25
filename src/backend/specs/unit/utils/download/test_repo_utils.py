"""
yt_diffuser.utils.download.repo_utils のテスト
"""
import pytest
from pytest_mock import MockerFixture

from types import SimpleNamespace
import tempfile

from yt_diffuser.config import AppConfig
from yt_diffuser.utils.download.repo_utils import *

def test_get_repo_info_from_url ():
    """
    get_repo_info_from_url()

    it:
        URLからリポジトリIDとリビジョン、ファイル名を取得する。
    """

    result = get_repo_info_from_url("https://huggingface.co/test/repo_id/blob/main/file.txt")
    assert result == {
        "repo_id": "test/repo_id",
        "revision": "main",
        "filename": "file.txt",
    }

    result = get_repo_info_from_url("https://huggingface.co/test/repo_id/blob/main/subdir/file.txt")
    assert result == {
        "repo_id": "test/repo_id",
        "revision": "main",
        "filename": "subdir/file.txt",
    }

    result = get_repo_info_from_url("https://huggingface.co/test/repo_id/blob/main")
    assert result == {
        "repo_id": "test/repo_id",
        "revision": "main",
        "filename": "",
    }

    result = get_repo_info_from_url("https://huggingface.co/test/repo_id")
    assert result == {
        "repo_id": "test/repo_id",
        "revision": "main",
        "filename": "",
    }

    with pytest.raises(ValueError):
        get_repo_info_from_url("https://hggingface.co/test/repo_id/blob/main/file.txt")


def test_get_storage_folder ():
    """
    get_storage_folder()

    it:
        保存先のディレクトリパスを取得する。
    """
    cache_dir = Path("/tmp")
    repo_id = "test/repo_id"

    storage_folder = get_storage_folder(cache_dir, repo_id)

    assert storage_folder == Path("/tmp/models--test--repo_id")


def test_save_ref_file (mocker: MockerFixture):
    """
    save_ref_file()

    it:
        - リビジョンがブランチ名やタグ名の場合、refsディレクトリにリビジョン名のファイルを作成する。
        - ファイルには参照先となるコミットハッシュを保存する。
        - リビジョンがコミットハッシュの場合は何もしない。
    """
    cache_dir = Path(tempfile.mkdtemp())
    repo_id = "test/repo_id"
    revision = "main"
    commit_hash = "revision"

    save_ref_file(cache_dir, repo_id, revision, commit_hash)

    storage_folder = cache_dir / "models--test--repo_id"

    assert (storage_folder / "refs" / "main").read_text() == "revision"

    revision = "revision"
    save_ref_file(cache_dir, repo_id, revision, commit_hash)

    assert not (storage_folder / "refs" / "revision").exists()


def dummy_hf_api_repo_info(*args, **kwargs):
    res = SimpleNamespace()
    res.sha = "revision"
    res.siblings = [
        SimpleNamespace(rfilename="scheduler/file1.txt"),
        SimpleNamespace(rfilename="text_encoder/file2.txt"),
        SimpleNamespace(rfilename="tokenizer/file3.txt"),
        SimpleNamespace(rfilename="unet/file4.txt"),
    ]
    return res

def test_get_repo_hash_and_files (mocker: MockerFixture):
    """
    get_repo_hash_and_files()

    it:
        リポジトリの情報を取得し、ダウンロード対象のファイルを絞り込む。
        また、ついでにcommit_hashも取得する。
    """
    mocker.patch("huggingface_hub.hf_api.HfApi.repo_info", side_effect=dummy_hf_api_repo_info)

    repo_id = "test/repo_id"
    revision = "main"
    folder_names = ["scheduler", "tokenizer", "unet"]

    commit_hash, files = get_repo_hash_and_files(repo_id, revision, folder_names)

    assert commit_hash == "revision"
    assert files == [
        "scheduler/file1.txt",
        "tokenizer/file3.txt",
        "unet/file4.txt",
    ]