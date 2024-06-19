from typing import Optional, Dict
from enum import Enum
import uuid

from pydantic import (
    BaseModel,
    Field,
    UUID4,
)

class WebEventType(Enum):
    """
    Webプロセスのイベントタイプ
    """
    GENERATOR = 'generator'

class WebEvent(BaseModel):
    """
    Webプロセスのイベント
    """
    id: UUID4 = Field(default_factory=uuid.uuid4)
    type: WebEventType
    args: Optional[Dict] = None

