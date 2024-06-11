"""
基本モデルのエンティティのテスト
"""
import pytest

from pathlib import Path

from huggingface_hub import scan_cache_dir

from yt_diffuser.types.path import AppPath
from yt_diffuser.domains.entity.model.base_model import BaseModelEntity, ModelType, ModelSource


class TestBaseModel:
    """
    BaseModel

    基本モデルのエンティティ
    """

    def test_base_model(self):
        """
        コンストラクタ
        """
        data = {
            'id': 'test_model',
            'screen_name': 'テストモデル',
            'source': ModelSource.HF.value,
            'type': ModelType.BASE_MODEL.value,
            'revisions': ['test_revision1', 'test_revision2'],
            'appends': {}
        }

        model = BaseModelEntity(**data)

        assert model.id == 'test_model'
        assert model.screen_name == 'テストモデル'
        assert model.source == ModelSource.HF
        assert model.type == ModelType.BASE_MODEL
        assert model.revisions == ['test_revision1', 'test_revision2']
        assert model.appends == {}

        data = {}

        model = BaseModelEntity(**data)

        assert model.id is None
        assert model.screen_name is None
        assert model.source == ModelSource.HF
        assert model.type == ModelType.BASE_MODEL
        assert model.revisions == []
        assert model.appends == {}
    
    def test_base_model_add_revision(self):
        """
        リビジョンを追加する
        """
        data = {
            'id': 'test_model',
            'screen_name': 'テストモデル',
            'source': ModelSource.HF.value,
            'type': ModelType.BASE_MODEL.value,
            'revisions': ['test_revision1', 'test_revision2'],
            'appends': {}
        }

        model = BaseModelEntity(**data)

        model.add_revision('test_revision3')

        assert model.revisions == ['test_revision1', 'test_revision2', 'test_revision3']
    
    def test_from_cached_repo_info(self):
        """
        Huggingface_hubのCacheRepoInfoからモデル情報を生成する

        """
        appPath = AppPath(base_dir=Path(__file__).parents[4] / 'data' / 'basic')
        hf_cache = scan_cache_dir(appPath.STORE_HF_MODEL_DIR)
        model_list = []
        for hf_repo in hf_cache.repos:
            model_list.append(BaseModelEntity.from_cached_repo_info(hf_repo))
        
        # 順不同なので、順番を揃える
        model_list = sorted(model_list, key=lambda x: x.id)
        
        assert len(model_list) == 2
        assert model_list[0].id == 'test/repo_id'
        assert model_list[0].screen_name == 'test/repo_id'
        assert model_list[0].source == ModelSource.HF
        assert model_list[0].type == ModelType.BASE_MODEL
        assert sorted(model_list[0].revisions) == ['bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb', 'test_revision']
        assert model_list[0].appends == {}

        assert model_list[1].id == 'test/repo_id2'
        assert model_list[1].screen_name == 'test/repo_id2'
        assert model_list[1].source == ModelSource.HF
        assert model_list[1].type == ModelType.BASE_MODEL
        assert sorted(model_list[1].revisions) == ['fp16', 'main']
        assert model_list[1].appends == {}


