""" ダウンロードプロセスのメイン処理
"""
import multiprocessing
import logging; logger = logging.getLogger(__name__)

from pydantic import BaseModel, ValidationError

from yt_diffuser.config import AppConfig
from yt_diffuser.store.enums import ModelClass
from yt_diffuser.download.base_model import download_base_model
from yt_diffuser.download.lora_model import download_lora_model


class DownloadRequest(BaseModel):
    repo_id:str
    revision:str
    model_class:ModelClass
    filename:str = None


def download_procedure (config:AppConfig, queue: multiprocessing.Queue, repo_id:str, revision:str, model_class:ModelClass, filename:str=None) -> None:
    """
    モデルファイルのダウンロードを実行する。

    本来 huggingface_hub.file_download.snapshot_download() を使うが、
    UIの都合そのままでは使えないため、似たような処理を実装する。

    """
    if config.debug:
        logging.basicConfig(level=logging.DEBUG)
    
    try:
        data = DownloadRequest(repo_id=repo_id, revision=revision, model_class=model_class, filename=filename).dict()
    except ValidationError as e:
        logger.error(e)
        return
    
    if data["model_class"] == ModelClass.BASE_MODEL:
        download_base_model(config, queue, data["repo_id"], data["revision"])
    
    elif data["model_class"] == ModelClass.LORA_MODEL:
        download_lora_model(config, queue, data["repo_id"], data["revision"], data["filename"])