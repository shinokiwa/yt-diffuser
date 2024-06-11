from logging import getLogger; logger = getLogger(__name__)

from fastapi import APIRouter, Depends

from pydantic import BaseModel, Field

from yt_diffuser.injector import get_depends
from yt_diffuser.types.web.response import ResponseModel, ResponseMeta
from yt_diffuser.usecases.web.generate.text_to_image_usecase import GenerateTextToImageUseCase

router = APIRouter()

class RequestData(BaseModel):
    """
    リクエストデータ
    """
    generate_count: int
    prompt: str
    negative_prompt: str
    scheduler: str

@router.post('/api/generate/text_to_image', response_model=ResponseModel[str])
def generate_text_to_image (data:RequestData, usecase:GenerateTextToImageUseCase = Depends(get_depends(GenerateTextToImageUseCase))):
    """
    text to imageで画像を生成する。
    """
    usecase.text_to_image(
        generate_count=data.generate_count,
        prompt=data.prompt,
        negative_prompt=data.negative_prompt,
        scheduler=data.scheduler
    )

    return ResponseModel[str](meta=ResponseMeta(), data='success')

