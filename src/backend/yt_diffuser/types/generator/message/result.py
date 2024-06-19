from enum import Enum

from pydantic import BaseModel

class GeneratorStatus(Enum):
    """
    ジェネレータステータス
    """
    IDLE = "IDLE"
    LOADING = "LOADING"
    LOADED = "LOADED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    EXIT = "EXIT"

class GenerateMessageResult(BaseModel):
    """
    生成プロセスからの結果メッセージ
    """
    status: GeneratorStatus = GeneratorStatus.IDLE

    base_model_id: str = ""
    last_file_name: str = ""

    generate_total: int = 0
    generate_count: int = 0
    steps_total: int = 0
    steps_count: int = 0
    percentage: float = 0
    elapsed: float = 0
    remaining: float = 0
    average: float = 0