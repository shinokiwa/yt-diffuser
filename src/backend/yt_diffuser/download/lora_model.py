"""
LoRAタイプのモデルをダウンロードする
"""
import multiprocessing
import logging; logger = logging.getLogger(__name__)

from yt_diffuser.config import AppConfig
from yt_diffuser.utils.download import (
    hf_hub_file_download,
    RepositoryNotFoundError,
    RevisionNotFoundError,
    EntryNotFoundError,
    HTTPError,
)
from yt_diffuser.utils.event import DownloadStatusEvent
from yt_diffuser.database import connect_database
from yt_diffuser.database.tables.model_info import save, ModelClass

def download_lora_model (config:AppConfig, queue: multiprocessing.Queue, repo_id:str, revision:str, filename:str):
    """
    モデルファイルのダウンロードを実行する。

    LoRAやControlNetなど、1ファイルのみで完結するモデルのダウンロードを行う。
    """
    if config.debug:
        logging.basicConfig(level=logging.DEBUG)

    logger.debug(f"download_procedure start: {repo_id}:{revision}")
    DownloadStatusEvent.send_process(queue, DownloadStatusEvent.Status.START, model_name=repo_id, revision=revision)

    # 指定したrepo_idとrevisionのmodel_index.jsonをダウンロードし、必要なファイルの一覧を取得する。
    try:
        hf_hub_file_download(
            config,
            repo_id=repo_id,
            revision=revision,
            filename=filename,
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

    # ダウンロードしたファイルの情報をDBに保存する。
    with connect_database(config.DB_FILE) as conn:
        save(conn, repo_id, revision, ModelClass.LORA_MODEL)
        conn.commit()