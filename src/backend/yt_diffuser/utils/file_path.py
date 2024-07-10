"""
ファイルパス関係のユーティリティ関数を提供するモジュール
"""
import logging; logger = logging.getLogger(__name__)
from typing import Union
from pathlib import Path

def is_child (parent:Union[str, Path], child:Union[str, Path]) -> bool:
    """
    childがparentの子孫かどうかを判定する。

    同一の場合もTrueとなる。
    """
    if not child.is_absolute():
        child = (parent / child).resolve()

    if isinstance(parent, str):
        parent = Path(parent)
    if isinstance(child, str):
        child = Path(child)

    return parent == child or parent in child.parents