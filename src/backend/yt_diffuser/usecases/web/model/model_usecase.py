from typing import Dict
import logging; logger = logging.getLogger(__name__)

from injector import inject

from yt_diffuser.domains.entity.model.all_model import AllModelList
from yt_diffuser.stores.model.model_store import ModelStore
from yt_diffuser.stores.process.interface import IProcessQueueStore

class ModelUseCase:
    """
    モデル情報を管理するユースケース
    """

    @inject
    def __init__(self, model_store:ModelStore, queue_store:IProcessQueueStore):
        """
        コンストラクタ
        
        Args:
            model_store (ModelStore): モデルストア
            queue_store (IProcessQueueStore): キューストア
        """
        self.model_store = model_store
        self.queue_store = queue_store

    def get_all(self) -> Dict:
        """
        全モデル情報を取得する
        """
        all_models = AllModelList()
        caches = self.model_store.read()
        for cache in caches:
            all_models.from_hf_cache_info(cache)
        
        return all_models.to_dict()
    