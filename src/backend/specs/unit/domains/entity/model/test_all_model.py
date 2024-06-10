import pytest

from pathlib import Path

from huggingface_hub import scan_cache_dir

from yt_diffuser.types.path import AppPath
from yt_diffuser.domains.entity.model.all_model import AllModelList

class TestAllModel:
    """
    AllModelList

    全モデルリストのエンティティ
    """

    def test_all_model(self):
        """
        コンストラクタ
        """
        data = {
            'base_models': [],
            'lora_models': [],
            'controlnet_models': []
        }

        all_model_list = AllModelList(data)

        assert all_model_list.base_models == []
        assert all_model_list.lora_models == []
        assert all_model_list.controlnet_models == []

    def test_all_model_add_base_model(self):
        """
        ベースモデルを追加する
        """
        data = {
            'base_models': [],
            'lora_models': [],
            'controlnet_models': []
        }

        all_model_list = AllModelList(data)

        assert all_model_list.base_models == []

        all_model_list.add_base_model('test_base_model')

        assert all_model_list.base_models == ['test_base_model']

    def test_all_model_from_hf_cache_info(self):
        """
        Huggingfaceキャッシュ情報からモデルリストを生成する
        """
        appPath = AppPath(base_dir=Path(__file__).parents[4] / 'data' / 'basic')
        hf_cache_info = scan_cache_dir(appPath.STORE_HF_MODEL_DIR)
        all_model_list = AllModelList().from_hf_cache_info(hf_cache_info)

        base_models = sorted(all_model_list.base_models, key=lambda x: x.model_name)
        assert base_models[0].model_name == 'test/repo_id'
        assert base_models[1].model_name == 'test/repo_id2'

        assert all_model_list.lora_models == []
        assert all_model_list.controlnet_models == []