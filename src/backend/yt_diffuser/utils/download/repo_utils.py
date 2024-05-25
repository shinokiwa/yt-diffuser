"""
hf_hub_downloadの定形処理をラッピングする。
"""
from typing import Tuple, Dict
import os
from pathlib import Path
import re
import logging; logger = logging.getLogger(__name__)

from huggingface_hub.file_download import repo_folder_name
from huggingface_hub.hf_api import HfApi
from huggingface_hub.constants import REPO_TYPE_MODEL
from huggingface_hub.utils import filter_repo_objects

def get_repo_info_from_url (url:str) -> Dict[str, str]:
    """
    URLからリポジトリIDとリビジョン、ファイル名を取得する。

    Args:
        url (str): URL httpsから始まるHuggingFace HubのURL
    
    Returns:
        dict: リポジトリID、リビジョン、ファイル名のdict
            - repo_id (str): リポジトリID
            - revision (str): リビジョン
            - filename (str): ファイル名
    """
    # HuggingFace HubのURLは
    # https://huggingface.co/{namespace}/{repo_name}/blob/{revision}/{filename}
    # という形式になっている。
    # /blob/ 以降はなくてもよい。

    regex = r"https://huggingface.co/([^/]+)/([^/]+)(?:/blob/([^/]+)(?:/(.+))?)?"
    match = re.match(regex, url)
    if match is None:
        raise ValueError(f"invalid url: {url}")
    
    namespace, repo_name, revision, filename = match.groups()
    return {
        "repo_id": f"{namespace}/{repo_name}",
        "revision": revision or "main",
        "filename": filename or "",
    }


def get_storage_folder (cache_dir:Path, repo_id:str) -> Path:
    """
    保存先のディレクトリパスを取得する。
    """
    return cache_dir / repo_folder_name(repo_id=repo_id, repo_type=REPO_TYPE_MODEL)


def save_ref_file (cache_dir:Path, repo_id:str, revision:str, commit_hash:str):
    """
    リビジョンがブランチ名やタグ名の場合、refsディレクトリにリビジョン名のファイルを作成する。
    ファイルには参照先となるコミットハッシュを保存する。
    リビジョンがコミットハッシュの場合は何もしない。
    """
    if revision != commit_hash:
        storage_folder = get_storage_folder(cache_dir, repo_id)

        ref_path = storage_folder / "refs" / revision
        ref_path.parent.mkdir(parents=True, exist_ok=True)
        with open(ref_path, "w") as f:
            f.write(commit_hash)


def get_repo_hash_and_files (
    repo_id: str,
    revision: str,
    folder_names: list,
) -> Tuple[str, list]:
    """
    リポジトリの情報を取得し、ダウンロード対象のファイルを絞り込む。
    また、ついでにcommit_hashも取得する。

    Args:
        cache_dir (Path): 保存先のディレクトリパス
        repo_id (str): リポジトリID
        revision (str): リビジョン
        folder_names (list): ダウンロード対象のフォルダ名のリスト
    
    Returns:
        tuple(str, list): commit_hash, ダウンロード対象のファイル名のリスト
    """
    allow_patterns = [os.path.join(k, "*") for k in folder_names]
    allow_patterns += [
        "diffusion_pytorch_model.bin",  # WEIGHTS_NAME 
        "config.json",                  # CONFIG_NAME 
        "scheduler_config.json",        # SCHEDULER_CONFIG_NAME
        "model.onnx",                   # ONNX_WEIGHTS_NAME
        "model_index.json",             # PIPELINE_CONFIG_NAME
    ]

    # make sure we don't download flax weights
    ignore_patterns = "*.msgpack"

    # HuggingFace Hub APIからすべてのファイル情報を取得する。
    api = HfApi()
    repo_info = api.repo_info(repo_id=repo_id, repo_type=REPO_TYPE_MODEL, revision=revision, token=None)

    # 取得したファイル情報から、許可パターンと拒否パターンを使って、ダウンロード対象のファイルを絞り込む。
    filtered_repo_files = list(
        filter_repo_objects(
            items=[f.rfilename for f in repo_info.siblings],
            allow_patterns=allow_patterns,
            ignore_patterns=ignore_patterns,
        )
    )
    commit_hash = repo_info.sha

    return commit_hash, filtered_repo_files