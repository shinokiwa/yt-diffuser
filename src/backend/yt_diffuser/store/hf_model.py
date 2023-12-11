""" HuggingFaceモデルストア
"""
from sqlite3 import Connection
from pathlib import Path

from huggingface_hub.file_download import repo_folder_name
from huggingface_hub.constants import REPO_TYPE_MODEL

# プログレスバーは表示しない
from huggingface_hub.utils import disable_progress_bars; disable_progress_bars()

from yt_diffuser.store.model import ModelStore, AppConfig
from yt_diffuser.store.db.op.models import MODEL_CLASS_NAME

class HFModelStore(ModelStore):
    """ HuggingFaceモデルストアクラス
    """
    class_num: int = MODEL_CLASS_NAME['HFModelStore']
    config_name: str = "model_index.json"

    def __init__(self, config:AppConfig,  repo_id: str, revision: str):
        path = repo_folder_name(repo_id=repo_id, repo_type=REPO_TYPE_MODEL)
        super().__init__(config, path, revision)

        self.repo_id = repo_id
    
    def set_path(self, path: str) -> None:
        self.path = self.config.STORE_HF_MODEL_DIR / path
    