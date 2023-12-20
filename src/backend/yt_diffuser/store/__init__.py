""" ストレージ操作を行うモジュール
"""

from .db import connect_database

MODEL_CLASS_NAME = { # models.class_name の区分値定義
    'ModelStore': 0,
    'HFModelStore': 1,
}

from .lock import StoreLock, StoreLockedError
from .base import Store
from .model import ModelStore
from .hf_model import HFModelStore
