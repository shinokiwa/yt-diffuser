from typing import Dict, List
from logging import getLogger; logger = getLogger(__name__)

from fastapi import APIRouter, Depends

from pydantic import BaseModel

from yt_diffuser.types.project import Project, ProjectLayer
from yt_diffuser.injector import get_depends
from yt_diffuser.types.web.response import ResponseModel, ResponseMeta
from yt_diffuser.usecases.web.project.project_usecase import ProjectUseCase

router = APIRouter()

class RequestData(BaseModel):
    """
    リクエストデータ
    """
    name:str
    width: int
    height: int

@router.post('/api/project', response_model=ResponseModel[str])
def post_project (data:RequestData, usecase:ProjectUseCase = Depends(get_depends(ProjectUseCase))):
    """
    プロジェクトを作成する。
    """
    usecase.create_project(project_name=data.name, width=data.width, height=data.height)

    response = ResponseModel[str](
        meta=ResponseMeta(),
        data='success'
    )

    return response

@router.get('/api/project', response_model=ResponseModel[List[Dict]])
def get_project_list (usecase:ProjectUseCase = Depends(get_depends(ProjectUseCase))):
    """
    プロジェクトのリストを取得する。
    """
    projects = usecase.get_project_list()

    response = ResponseModel[List[Dict]](
        meta=ResponseMeta(),
        data=[{
            'name': project.project_name,
            'width': project.width,
            'height': project.height
        } for project in projects]
    )

    return response

@router.get('/api/project/{name}', response_model=ResponseModel[Project])
def get_project (name:str, usecase:ProjectUseCase = Depends(get_depends(ProjectUseCase))):
    """
    プロジェクトを取得する。
    """
    project = usecase.get_project(name)

    response = ResponseModel[Project](
        meta=ResponseMeta(),
        data=project
    )

    return response

@router.delete('/api/project/{name}', response_model=ResponseModel[str])
def delete_project (name:str, usecase:ProjectUseCase = Depends(get_depends(ProjectUseCase))):
    """
    プロジェクトを削除する。
    """
    usecase.remove_project(name)

    response = ResponseModel[str](
        meta=ResponseMeta(),
        data='success'
    )

    return response