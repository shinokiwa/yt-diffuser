"""
ベースモデルのダウンロード処理
"""
import multiprocessing
import json
import logging; logger = logging.getLogger(__name__)

from tqdm.contrib.concurrent import thread_map

from yt_diffuser.config import AppConfig
from yt_diffuser.utils.download import (
    hf_hub_file_download,
    save_ref_file,
    get_repo_hash_and_files,
    RepositoryNotFoundError,
    RevisionNotFoundError,
    EntryNotFoundError,
    HTTPError,
)
from yt_diffuser.utils.event import DownloadStatusEvent
from yt_diffuser.download.tqdm import DownloadProgress

def download_base_model (config:AppConfig, queue: multiprocessing.Queue, repo_id:str, revision:str):
    """
    モデルファイルのダウンロードを実行する。

    本来 huggingface_hub.file_download.snapshot_download() を使うが、
    UIの都合そのままでは使えないため、似たような処理を実装する。

    """
    if config.debug:
        logging.basicConfig(level=logging.DEBUG)

    logger.debug(f"download_procedure start: {repo_id}:{revision}")
    DownloadStatusEvent.send_process(queue, DownloadStatusEvent.Status.START, model_name=repo_id, revision=revision)

    cache_dir = config.STORE_HF_MODEL_DIR

    # 指定したrepo_idとrevisionのmodel_index.jsonをダウンロードし、必要なファイルの一覧を取得する。
    try:
        config_file = hf_hub_file_download(
            config,
            repo_id=repo_id,
            revision=revision,
            filename="model_index.json",
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
        DownloadStatusEvent.send_process(queue, DownloadStatusEvent.Status.ERROR, model_name=repo_id, revision=revision, error=str(e))
        return
    
    # model_index.jsonに記載されている項目のうち、_から始まらない項目をダウンロード対象のフォルダ名として取得する。
    with open(config_file, "r", encoding="utf-8") as reader:
        text = reader.read()

    config_dict = json.loads(text)
    folder_names = [k for k in config_dict.keys() if not k.startswith("_")]

    # ダウンロード対象のファイル一覧とコミットハッシュを取得する。
    commit_hash, repo_files = get_repo_hash_and_files(
        repo_id=repo_id,
        revision=revision,
        folder_names=folder_names,
    )

    # 必要ならリビジョン参照ファイルを作成する。
    save_ref_file(cache_dir, repo_id, revision, commit_hash)

    # コミットハッシュを指定してダウンロードする。
    # 既に同一のコミットハッシュでダウンロード済みの場合は、
    # ネットワーク通信は発生しない。
    def _inner_hf_hub_download(repo_file: str):
        return hf_hub_file_download(
            config,
            repo_id=repo_id,
            revision=commit_hash,
            filename=repo_file,
        )

    thread_map(
        _inner_hf_hub_download,
        repo_files,
        max_workers=8,
        tqdm_class=DownloadProgress,
        queue=queue,
        model_name=repo_id,
        revision=revision,
    )

    DownloadStatusEvent.send_process(queue, DownloadStatusEvent.Status.COMPLETE, model_name=repo_id, revision=revision)
    logger.debug(f"download_procedure complete: {repo_id}:{revision}")