from typing import Dict, List
import logging; logger = logging.getLogger(__name__)

from fastapi import APIRouter, Depends

from pydantic import BaseModel

from yt_diffuser.injector import get_depends
from yt_diffuser.types.web.response import ResponseModel, ResponseMeta
from yt_diffuser.usecases.web.tempimage.tempimage_usecase import TempImageUseCase

router = APIRouter()

class ResponseData(BaseModel):
    """
    レスポンスデータ
    """
    list: List[str] = []


@router.get('/api/temp/index', response_model=ResponseModel[ResponseData])
def get_temp_index (usecase:TempImageUseCase = Depends(get_depends(TempImageUseCase))):

    list = usecase.get_index()
    return ResponseModel[ResponseData](
        meta=ResponseMeta(),
        data=ResponseData(list=list)
    )