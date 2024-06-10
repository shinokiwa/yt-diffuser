"""
マルチプロセス関係の列挙型を定義するモジュール
"""
from enum import Enum

class ProcessKey(Enum):
    """
    プロセスのキーを列挙する列挙型
    """
    GENERATOR = 'generator'
    DOWNLOADER = 'downloader'