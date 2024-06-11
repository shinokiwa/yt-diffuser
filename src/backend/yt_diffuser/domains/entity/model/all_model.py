"""
全モデルリストのエンティティ
"""
from typing import List, Dict

from huggingface_hub.utils import HFCacheInfo

from .base_model import BaseModelEntity

class AllModelList:
    """
    全モデルリストのエンティティ
    """

    def __init__(self, data: Dict = {}):
        self.base_models:List[BaseModelEntity] = []

        self.lora_models = []
        self.controlnet_models = []

        for base_model_data in data.get('base_models', []):
            self.base_models.append(BaseModelEntity(**base_model_data))
    
    def add_base_model(self, base_model:BaseModelEntity):
        """
        ベースモデルを追加する
        """
        self.base_models.append(base_model)

    def from_hf_cache_info(self, hf_cache_info: HFCacheInfo):
        """
        Huggingfaceキャッシュ情報からモデルリストを生成する
        """

        for hf_repo in hf_cache_info.repos:
            self.add_base_model(BaseModelEntity.from_cached_repo_info(hf_repo))

        return self
    
    def to_dict(self) -> Dict:
        """
        エンティティを辞書に変換する
        """
        return {
            'base_models': [base_model.model_dump() for base_model in self.base_models],
            'lora_models': self.lora_models,
            'controlnet_models': self.controlnet_models
        }