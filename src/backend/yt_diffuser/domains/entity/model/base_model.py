"""
基本モデルのエンティティ
"""
from typing import List, Dict

from pydantic import BaseModel
from huggingface_hub.utils import CachedRepoInfo

from yt_diffuser.types.enum.model import ModelType, ModelSource

class BaseModelEntity(BaseModel):
    """
    ベースモデルのエンティティ
    """

    id:str = None
    """
    モデル名
    """

    screen_name:str = None
    """
    表示名
    """

    source:ModelSource = ModelSource.HF
    """
    ソース
    """

    type:ModelType = ModelType.BASE_MODEL
    """
    モデル種類
    """

    revisions:List[str] = []
    """
    リビジョン
    """

    appends:Dict = {}
    """
    追加情報

    @todo いまのところ使っていないので型定義していないが、使う場合は型定義する
    """
    
    def add_revision(self, revision:str):
        """
        リビジョンを追加する
        """
        self.revisions.append(revision)
    
    @classmethod
    def from_cached_repo_info(cls, repo_info:CachedRepoInfo) -> 'BaseModelEntity':
        """
        Huggingface_hubのCacheRepoInfoからモデル情報を生成する

        args:
            repo_info: CachedRepoInfo キャッシュリポジトリ情報

        """
        model = BaseModelEntity( 
            id=repo_info.repo_id,
            screen_name= repo_info.repo_id,
            source= ModelSource.HF.value,
            type= ModelType.BASE_MODEL.value,
            revisions= [],
            appends= {}
        )


        for revision in repo_info.revisions:
            if revision.refs is None or len(revision.refs) == 0:
                model.add_revision(revision.commit_hash)
            else:
                for ref in revision.refs:
                    model.add_revision(ref)
        
        return model