from typing import Union
import uuid

from pydantic import BaseModel, Field, UUID4

class ProjectLayer(BaseModel):
    """
    プロジェクトのレイヤー情報を保持するクラス
    """

    layer_id: Union[UUID4, str] = Field(default_factory=uuid.uuid4)
    layer_name: str

    image: str = None
    i2i: str = None
    mask: str = None