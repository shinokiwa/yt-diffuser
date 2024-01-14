"""
モデル情報クラス
"""
from typing import List, Dict
from logging import getLogger; logger = getLogger(__name__)

from yt_diffuser.store.enums import ModelClass, ModelSource

class ModelInfo:
    """
    モデル情報クラス
    """

    def __init__ (self,
        model_name:str,
        model_class:ModelClass,
        source: ModelSource,
    ):
        self.model_name:str = model_name
        self.model_class:str = model_class
        self.source:str = source
        self.revisions:List[str] = []
        self.screen_name:str = None
        self.appends:Dict[str, str] = {}

        if self.model_class == ModelClass.BASE_MODEL:
            self.appends['pipeline_name'] = ''
            self.appends['precision'] = ''
        
        elif self.model_class == ModelClass.LORA_MODEL:
            self.appends['weight_name'] = ''
        
        else:
            raise ValueError(f"ModelClass is invalid: {self.model_class}")

    def add_revision (self, revision:str):
        """
        リビジョンを追加する。
        """
        self.revisions.append(revision)

    def set_screen_name (self, screen_name:str):
        """
        スクリーン名を設定する。
        """
        self.screen_name = screen_name


    def set_append (self, key:str, value:str):
        """
        付加情報を設定する。
        """
        self.appends[key] = value


    def to_dict (self):
        """
        辞書に変換する。
        """
        return {
            'model_name': self.model_name,
            'model_class': self.model_class.value,
            'source': self.source.value,
            'revisions': self.revisions,
            'screen_name': self.screen_name,
            'appends': self.appends,
        }