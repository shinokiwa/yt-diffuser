"""
APIのレスポンス型
"""
from typing import Generic, TypeVar
from pydantic import BaseModel

class ResponseMeta(BaseModel):
    """
    レスポンスのメタ情報を定義するクラス
    """
    status: int = 200
    message: str = None
    error: str = None

T = TypeVar('T')

class ResponseModel(BaseModel, Generic[T]):
    """
    APIのレスポンスを定義するクラス
    """
    meta: ResponseMeta = ResponseMeta()
    data: T = None
