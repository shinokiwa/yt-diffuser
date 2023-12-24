"""
HuggingFaceモデルストア
"""
from sqlite3 import Connection
from pathlib import Path

from huggingface_hub.file_download import repo_folder_name
from huggingface_hub.constants import REPO_TYPE_MODEL

# プログレスバーは表示しない
from huggingface_hub.utils import disable_progress_bars; disable_progress_bars()

from yt_diffuser.store.model import ModelStore, AppConfig

class HFModelStore(ModelStore):
    """
    HuggingFaceモデルストアクラス
    """

    def __init__(self, config: AppConfig,
                    model_name: str,
                    revision: str,
                    commit_hash: str = None,
                    ref: str = None,
                    screen_name: str = None,
        ):
        self.base_dir: Path = config.STORE_HF_MODEL_DIR
        self.model_name: str = model_name  
        self.revision: str = revision
        self.commit_hash: str = commit_hash
        self.ref: str = ref
        self.screen_name: str = screen_name

    
    @property
    def path(self) -> Path:
        return self.base_dir / repo_folder_name(repo_id=self.model_name, repo_type=REPO_TYPE_MODEL)
    