from typing import List, Annotated
import logging; logger = logging.getLogger(__name__)

from fastapi import APIRouter, Depends, Path

from pydantic import BaseModel

from yt_diffuser.injector import get_depends
from yt_diffuser.types.web.response import ResponseModel, ResponseMeta
from yt_diffuser.usecases.web.tempimage.tempimage_usecase import TempImageUseCase

router = APIRouter()

@router.delete('/api/temp/{filename}', response_model=ResponseModel[str])
def get_temp_index (
    filename: str,
    usecase:TempImageUseCase = Depends(get_depends(TempImageUseCase))
):

    usecase.delete(filename=filename)

    return ResponseModel[str](
        meta=ResponseMeta(),
        data="ok"
    )

