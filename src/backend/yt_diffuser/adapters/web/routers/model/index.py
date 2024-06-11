from typing import Dict, List
from logging import getLogger; logger = getLogger(__name__)

from fastapi import APIRouter, Depends

from pydantic import BaseModel, Field

from yt_diffuser.injector import get_depends
from yt_diffuser.types.web.response import ResponseModel, ResponseMeta
from yt_diffuser.types.enum.model import ModelType, ModelSource
from yt_diffuser.usecases.web.model.model_usecase import ModelUseCase

router = APIRouter()

class ResponseDataModel(BaseModel):
    """
    レスポンスデータモデル個別
    """
    id:str
    screen_name: str
    source: ModelSource
    type: ModelType
    revisions: List[str]
    appends: Dict

class ResponseData(BaseModel):
    """
    レスポンスデータ
    """
    base_models: List[ResponseDataModel] = []
    lora_models: List[ResponseDataModel] = []
    controlnet_models: List[ResponseDataModel] = []

@router.get('/api/model', response_model=ResponseModel[ResponseData])
def get_model (usecase:ModelUseCase = Depends(get_depends(ModelUseCase))):
    """
    保存済みのモデル一覧を取得する。
    """
    data = usecase.get_all()

    base_models = [ResponseDataModel(**model) for model in data['base_models']]
    lora_models = [ResponseDataModel(**model) for model in data['lora_models']]
    controlnet_models = [ResponseDataModel(**model) for model in data['controlnet_models']]

    response = ResponseModel[ResponseData](
        meta=ResponseMeta(),
        data=ResponseData(base_models=base_models, lora_models=lora_models, controlnet_models=controlnet_models)
    )

    return response