"""
エラーまわりの集約
一括でインポートできるようにするためのファイル
"""

from requests import (
    HTTPError
)

from huggingface_hub.utils import (
    EntryNotFoundError,
    RepositoryNotFoundError,
    RevisionNotFoundError,
)
