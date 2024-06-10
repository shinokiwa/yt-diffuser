from logging import getLogger; logger = getLogger(__name__)

from fastapi import APIRouter, Depends

from pydantic import BaseModel, Field

from yt_diffuser.injector import get_depends
from yt_diffuser.types.web.response import ResponseModel, ResponseMeta
from yt_diffuser.usecases.web.model.load_usecase import ModelLoadUseCase

router = APIRouter()


class RequestData(BaseModel):
    """
    リクエストデータ
    """
    base_model_name:str
    base_revision: str
    compile: bool


@router.post('/api/model/load', response_model=ResponseModel[str])
def load_model (
    data:RequestData,
    loader:ModelLoadUseCase = Depends(get_depends(ModelLoadUseCase))
):
    """
    モデルを読み込む。
    """
    loader.load(data.base_model_name, data.base_revision, data.compile)

    return ResponseModel[str](meta=ResponseMeta(), data='success')
