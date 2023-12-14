""" ダウンロードプロセスのメイン処理
"""
import multiprocessing
import os
import json
from requests import HTTPError
import logging; logger = logging.getLogger(__name__)

from tqdm.contrib.concurrent import thread_map
from huggingface_hub.file_download import (
    hf_hub_download,
    repo_folder_name,
    REGEX_COMMIT_HASH
)
from huggingface_hub.utils import (
    EntryNotFoundError, RepositoryNotFoundError, RevisionNotFoundError,
    filter_repo_objects
)
# プログレスバーは表示しない
from huggingface_hub.utils import disable_progress_bars; disable_progress_bars()
from huggingface_hub.constants import REPO_TYPE_MODEL
from huggingface_hub.hf_api import HfApi

from yt_diffuser.config import AppConfig
from yt_diffuser.utils.tqdm import WorkerProgress
from yt_diffuser.utils.message_queue import send_message
from yt_diffuser.store import connect_database, HFModelStore

def download_procedure (config:AppConfig, queue: multiprocessing.Queue, repo_id:str, revision:str):
    """
    モデルファイルのダウンロードを実行する。

    本来 huggingface_hub.file_download.snapshot_download() を使うが、
    UIの都合そのままでは使えないため、似たような処理を実装する。

    """
    if config.debug:
        logging.basicConfig(level=logging.DEBUG)

    logger.debug(f"download_procedure start: {repo_id}:{revision}")
    send_message(queue, "download-start", target=f"{repo_id}:{revision}")

    cache_dir = config.STORE_HF_MODEL_DIR
    local_files_only = config.offline == True

    # 指定したrepo_idとrevisionのmodel_index.jsonをダウンロードする。
    try:
        config_file = hf_hub_download(
            repo_id,
            repo_type=REPO_TYPE_MODEL,
            filename="model_index.json",
            cache_dir=cache_dir,
            force_download=False,
            proxies=None,
            resume_download=False,
            local_files_only=local_files_only,
            use_auth_token=None,
            #user_agent=user_agent,
            subfolder=None,
            revision=revision,
        )
    except (
        RepositoryNotFoundError,
        RevisionNotFoundError,
        EntryNotFoundError,
        HTTPError,
        ValueError,
        EnvironmentError
    ) as e:
        logger.error (f"download_procedure error! {e.__class__.__name__}")
        send_message(queue, "download-error", target=e.__class__.__name__)
        return

    # model_index.jsonに記載されている項目のうち、_から始まらない項目をダウンロード対象のフォルダ名として取得する。
    with open(config_file, "r", encoding="utf-8") as reader:
        text = reader.read()

    config_dict = json.loads(text)

    folder_names = [k for k in config_dict.keys() if not k.startswith("_")]
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

    # 必要な全ファイルをダウンロード
    # snapshot_downloadがそのままでは使えないので、コピペして修正

    storage_folder = os.path.join(cache_dir, repo_folder_name(repo_id=repo_id, repo_type=REPO_TYPE_MODEL))

    if local_files_only:
        if REGEX_COMMIT_HASH.match(revision):
            commit_hash = revision
        else:
            # retrieve commit_hash from file
            ref_path = os.path.join(storage_folder, "refs", revision)
            with open(ref_path) as f:
                commit_hash = f.read()

        snapshot_folder = os.path.join(storage_folder, "snapshots", commit_hash)

        if os.path.exists(snapshot_folder) == False:
            logger.error (f"download_procedure error! {e.__class__.__name__}")
            send_message(queue, "download-error", target=e.__class__.__name__)

        return

    # HuggingFace Hub APIからすべてのファイル情報を取得する。
    api = HfApi()
    repo_info = api.repo_info(repo_id=repo_id, repo_type=REPO_TYPE_MODEL, revision=revision, token=None)
    assert repo_info.sha is not None, "Repo info returned from server must have a revision sha."

    # 取得したファイル情報から、許可パターンと拒否パターンを使って、ダウンロード対象のファイルを絞り込む。
    filtered_repo_files = list(
        filter_repo_objects(
            items=[f.rfilename for f in repo_info.siblings],
            allow_patterns=allow_patterns,
            ignore_patterns=ignore_patterns,
        )
    )
    commit_hash = repo_info.sha

    # リビジョンはコミットハッシュである必要があるが、
    # ブランチ名やタグ名を指定することもできる。
    # その場合はrefsディレクトリのブランチ名やタグ名のファイルに
    # コミットハッシュを参照として保存する。
    if revision != commit_hash:
        ref_path = os.path.join(storage_folder, "refs", revision)
        os.makedirs(os.path.dirname(ref_path), exist_ok=True)
        with open(ref_path, "w") as f:
            f.write(commit_hash)

    # コミットハッシュを指定してダウンロードする。
    # 既に同一のコミットハッシュでダウンロード済みの場合は、
    # ネットワーク通信は発生しない。
    def _inner_hf_hub_download(repo_file: str):
        return hf_hub_download(
            repo_id,
            filename=repo_file,
            repo_type=REPO_TYPE_MODEL,
            revision=commit_hash,
            endpoint=None,
            cache_dir=cache_dir,
            local_dir=None,
            local_dir_use_symlinks="auto",
            library_name=None,
            library_version=None,
            user_agent=None,
            proxies=None,
            resume_download=True,
            force_download=False,
            token=None,
        )

    thread_map(
        _inner_hf_hub_download,
        filtered_repo_files,
        max_workers=8,
        tqdm_class=WorkerProgress,
        event="download",
        queue=queue,
        target=f"{repo_id}:{revision}",
    )

    # ダウンロードしたファイルをモデルストアに保存する。
    conn = connect_database(config.DB_FILE)
    hf_model_store = HFModelStore(config, repo_id=repo_id, revision=revision)
    hf_model_store.save(conn)
    conn.commit()

    send_message(queue, "download-complete", target=f"{repo_id}:{revision}")

    logger.debug(f"download_procedure complete: {repo_id}:{revision}")