
from yt_diffuser.types.enum.model import PipelineClass

class PipelineEntity:
    """
    パイプラインを制御するエンティティ
    """
    def __init__(self):
        pass

    def get_entity(self, pipeline_class:PipelineClass):
        """
        パイプラインエンティティを取得する

        Args:
            model_type (ModelClass): モデルクラス
        """
        return {
            "pipeline_id": self.pipeline_id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }