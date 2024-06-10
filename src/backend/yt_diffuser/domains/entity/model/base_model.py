"""
基本モデルのエンティティ
"""
from typing import List, Dict

from huggingface_hub.utils import CachedRepoInfo

from yt_diffuser.types.enum.model import ModelType, ModelSource

class BaseModel:
    """
    ベースモデル
    """
    def __init__(self, data:Dict):
        """
        コンストラクタ

        args:
            data: Dict モデルデータ
        """

        self.od = data.get('id')
        """
        モデル名
        """

        self.screen_name = data.get('screen_name')
        """
        表示名
        """

        self.source = ModelSource(data.get('source', ModelSource.HF.value))
        """
        ソース
        """

        self.model_class:ModelType = ModelType(data.get('model_class', ModelType.BASE_MODEL.value))
        """
        モデルクラス
        """

        self.revisions = []
        """
        リビジョン
        """

        if isinstance(data.get('revisions'), list):
            for revision in data.get('revisions'):
                self.revisions.append(revision)

        self.appends:Dict = data.get('appends', {})
        """
        追加情報

        @todo いまのところ使っていないので型定義していないが、使う場合は型定義する
        """
    
    def add_revision(self, revision:str):
        """
        リビジョンを追加する
        """
        self.revisions.append(revision)
    
    def to_dict(self) -> Dict:
        """
        エンティティを辞書に変換する
        """
        return {
            'id': self.id,
            'screen_name': self.screen_name,
            'source': self.source.value,
            'model_class': self.model_class.value,
            'revisions': self.revisions,
            'appends': self.appends
        }
    
    @classmethod
    def from_cached_repo_info(cls, repo_info:CachedRepoInfo) -> 'BaseModel':
        """
        Huggingface_hubのCacheRepoInfoからモデル情報を生成する

        args:
            repo_info: CachedRepoInfo キャッシュリポジトリ情報

        """
        model = BaseModel({ 
            'model_name': repo_info.repo_id,
            'screen_name': repo_info.repo_id,
            'source': ModelSource.HF.value,
            'model_class': ModelType.BASE_MODEL.value,
            'revisions': [],
            'appends': {}
        })


        for revision in repo_info.revisions:
            if revision.refs is None or len(revision.refs) == 0:
                model.add_revision(revision.commit_hash)
            else:
                for ref in revision.refs:
                    model.add_revision(ref)
        
        return model