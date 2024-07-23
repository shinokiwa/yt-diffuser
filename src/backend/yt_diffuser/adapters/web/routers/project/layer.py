from logging import getLogger; logger = getLogger(__name__)
import tempfile
from pathlib import Path

from fastapi import APIRouter, Depends, File, UploadFile

from pydantic import BaseModel

from yt_diffuser.injector import get_depends
from yt_diffuser.types.web.response import ResponseModel, ResponseMeta
from yt_diffuser.types.project import ProjectLayer
from yt_diffuser.usecases.web.project.layer_usecase import ProjectLayerUseCase

router = APIRouter()

class RequestData(BaseModel):
    """
    リクエストデータ
    """
    layer_name:str

@router.post('/api/project/{project_name}/layer', response_model=ResponseModel[str])
def post_layer (project_name:str, data:RequestData, usecase:ProjectLayerUseCase = Depends(get_depends(ProjectLayerUseCase))):
    """
    レイヤーを作成する。
    """
    layer = ProjectLayer(layer_name=data.layer_name)
    usecase.add_layer(project_name=project_name, layer=layer)

    response = ResponseModel[str](
        meta=ResponseMeta(),
        data='success'
    )

    return response

@router.post('/api/project/{project_name}/layer/{layer_id}/image', response_model=ResponseModel[str])
def post_image (
    project_name:str,
    layer_id:str,
    file:UploadFile = File(...),
    usecase:ProjectLayerUseCase = Depends(get_depends(ProjectLayerUseCase))
):
    """
    画像をアップロードする。
    """

    # ファイルを一時ディレクトリに保存
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir) / file.filename
        ext = temp_path.suffix
        with temp_path.open('wb') as f:
            f.write(file.file.read())
        
        usecase.upload_image(project_name, layer_id, "image" + ext, str(temp_path))

    response = ResponseModel[str](
        meta=ResponseMeta(),
        data='success'
    )

    return response

@router.delete('/api/project/{project_name}/layer/{layer_id}', response_model=ResponseModel[str])
def delete_layer (name:str, usecase:ProjectLayerUseCase = Depends(get_depends(ProjectLayerUseCase))):
    """
    レイヤーを削除する。
    """
    usecase.remove_project(name)

    response = ResponseModel[str](
        meta=ResponseMeta(),
        data='success'
    )

    return response