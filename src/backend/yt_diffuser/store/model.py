""" モデルストアクラス
"""
from pathlib import Path

from yt_diffuser.store.base import Store
from yt_diffuser.constant import STORE_MODEL_DIR

class ModelStore(Store):
    """ モデルストアクラス
    """
    base_dir: Path = STORE_MODEL_DIR
