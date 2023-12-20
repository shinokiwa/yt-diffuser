"""
HuggingFaceモデルストア
"""
from sqlite3 import Connection
from pathlib import Path

from huggingface_hub import scan_cache_dir, HFCacheInfo
from huggingface_hub.file_download import repo_folder_name, REGEX_COMMIT_HASH
from huggingface_hub.utils import (
    EntryNotFoundError,
    RepositoryNotFoundError,
    RevisionNotFoundError
)
from huggingface_hub.constants import REPO_TYPE_MODEL
from huggingface_hub.hf_api import (
    HfApi,
    ModelInfo,
    RepoFile
)

# プログレスバーは表示しない
from huggingface_hub.utils import disable_progress_bars; disable_progress_bars()

from yt_diffuser.store import MODEL_CLASS_NAME
from yt_diffuser.store.model import ModelStore, AppConfig
from yt_diffuser.store.db.op.models import get as get_model
from yt_diffuser.store.db.op.models_hf_refs import get as get_model_hf_refs

class HFModelStore(ModelStore):
    """
    HuggingFaceモデルストアクラス
    """
    class_num: int = MODEL_CLASS_NAME['HFModelStore']

    def __init__(self, config:AppConfig,  repo_id: str, revision: str):
        super().__init__(config, repo_id, revision)

        self.commit_hash:str = None
        self.repo_info:ModelInfo = None

    
    @property
    def path(self) -> Path:
        return self.config.STORE_HF_MODEL_DIR / repo_folder_name(repo_id=self.store_name, repo_type=REPO_TYPE_MODEL)
    

    @classmethod
    def scan_cache_dir(cls, config:AppConfig) -> HFCacheInfo:
        """
        キャッシュディレクトリをスキャンし、モデルストアのリストを取得する。
        """
        return scan_cache_dir(config.STORE_HF_MODEL_DIR)
