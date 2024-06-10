"""
/api/form
フォーム内容の保存と取得を行う
"""
from typing import Dict

from logging import getLogger; logger = getLogger(__name__)

from fastapi import APIRouter, Depends

from yt_diffuser.injector import get_depends
from yt_diffuser.types.web.response import ResponseModel, ResponseMeta
from yt_diffuser.usecases.web.form.form_usecase import FormUseCase

router = APIRouter()

@router.get("/api/form", response_model=ResponseModel[Dict])
def get_form(usecase:FormUseCase = Depends(get_depends(FormUseCase))):
    """
    最後に保存されたフォーム内容を取得する

    Returns:
        ResponseModel[Dict]: フォーム内容
    """
    data = usecase.read()

    response = ResponseModel[Dict](
        meta=ResponseMeta(),
        data=data
    )
    return response

@router.post("/api/form", response_model=ResponseModel[Dict])
def post_form(data:Dict, usecase:FormUseCase = Depends(get_depends(FormUseCase))):
    """
    フォーム内容を保存する

    Args:
        data (Dict): フォーム内容

    Returns:
        ResponseModel[Dict]: フォーム内容
    """
    usecase.write(data)

    response = ResponseModel[Dict](
        meta=ResponseMeta(),
        data=data
    )
    return response