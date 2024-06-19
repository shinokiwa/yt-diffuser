from typing import Dict, Optional
import uuid

from pydantic import (
    BaseModel,
    Field,
    UUID4,
)

from .command import GeneratorCommand

class GenerateMessage(BaseModel):
    """
    生成プロセスへのメッセージ
    """
    id: UUID4 = Field(default_factory=uuid.uuid4)
    command: GeneratorCommand
    args: Optional[Dict] = None
