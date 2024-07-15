from typing import Dict, List, Optional
from logging import getLogger; logger = getLogger(__name__)

from fastapi import APIRouter, Depends, File, UploadFile

from pydantic import BaseModel

from yt_diffuser.injector import get_depends
from yt_diffuser.types.web.response import ResponseModel, ResponseMeta
from yt_diffuser.usecases.web.project.project_usecase import ProjectUseCase

router = APIRouter()

class RequestData(BaseModel):
    """
    リクエストデータ
    """
    layer_name:str

@router.post('/api/project/{project_name}/layer', response_model=ResponseModel[str])
def post_layer (data:RequestData, usecase:ProjectUseCase = Depends(get_depends(ProjectUseCase))):
    """
    レイヤーを作成する。
    """
    usecase.create_project(name=data.name, width=data.width, height=data.height)

    response = ResponseModel[str](
        meta=ResponseMeta(),
        data='success'
    )

    return response

@router.delete('/api/project/{project_name}/layer/{layer_id}', response_model=ResponseModel[str])
def delete_layer (name:str, usecase:ProjectUseCase = Depends(get_depends(ProjectUseCase))):
    """
    レイヤーを削除する。
    """
    usecase.remove_project(name)

    response = ResponseModel[str](
        meta=ResponseMeta(),
        data='success'
    )

    return response