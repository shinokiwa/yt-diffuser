"""
yt_diffuser.store.last_usedモジュールのテスト
"""
import pytest
from pathlib import Path
import tempfile

from specs.mock.mock_config import mock_config, AppConfig

from yt_diffuser.store.last_used import *

class TestLastUsedModel:

    def test_init (self):
        """
        コンストラクタのテスト
        """
        model = LastUsedModel()
        assert model.base_model_name == ""
        assert model.base_model_revision == ""
        assert model.lora_model_name == ""
        assert model.lora_model_revision == ""
        assert model.lora_model_weight_name == ""
        assert model.controlnet_model_name == ""
        assert model.controlnet_model_revision == ""
        assert model.controlnet_model_weight_name == ""
        assert model.compiled == False

        model = LastUsedModel(
            base_model_name="base_model_name",
            base_model_revision="base_model_revision",
            lora_model_name="lora_model_name",
            lora_model_revision="lora_model_revision",
            lora_model_weight_name="lora_model_weight_name",
            controlnet_model_name="controlnet_model_name",
            controlnet_model_revision="controlnet_model_revision",
            controlnet_model_weight_name="controlnet_model_weight_name",
            compiled=True
        )
        assert model.base_model_name == "base_model_name"
        assert model.base_model_revision == "base_model_revision"
        assert model.lora_model_name == "lora_model_name"
        assert model.lora_model_revision == "lora_model_revision"
        assert model.lora_model_weight_name == "lora_model_weight_name"
        assert model.controlnet_model_name == "controlnet_model_name"
        assert model.controlnet_model_revision == "controlnet_model_revision"
        assert model.controlnet_model_weight_name == "controlnet_model_weight_name"
        assert model.compiled == True

    def test_to_dict (self):
        """
        to_dict

        it:
            - 辞書に変換する。
        """
        model = LastUsedModel(
            base_model_name="base_model_name",
            base_model_revision="base_model_revision",
            lora_model_name="lora_model_name",
            lora_model_revision="lora_model_revision",
            lora_model_weight_name="lora_model_weight_name",
            controlnet_model_name="controlnet_model_name",
            controlnet_model_revision="controlnet_model_revision",
            controlnet_model_weight_name="controlnet_model_weight_name",
            compiled=True
        )
        assert model.to_dict() == {
            'base': {
                'model_name': 'base_model_name',
                'revision': 'base_model_revision'
            },
            'lora': {
                'model_name': 'lora_model_name',
                'revision': 'lora_model_revision',
                'weight_name': 'lora_model_weight_name'
            },
            'controlnet': {
                'model_name': 'controlnet_model_name',
                'revision': 'controlnet_model_revision',
                'weight_name': 'controlnet_model_weight_name'
            },
            'compiled': True
        }
    
    def test_from_dict (self):
        """
        from_dict

        it:
            - 辞書からインスタンスを生成する。
        """
        model = LastUsedModel.from_dict({
            'base': {
                'model_name': 'base_model_name',
                'revision': 'base_model_revision'
            },
            'lora': {
                'model_name': 'lora_model_name',
                'revision': 'lora_model_revision',
                'weight_name': 'lora_model_weight_name'
            },
            'controlnet': {
                'model_name': 'controlnet_model_name',
                'revision': 'controlnet_model_revision',
                'weight_name': 'controlnet_model_weight_name'
            },
            'compiled': True
        })
        assert model.base_model_name == "base_model_name"
        assert model.base_model_revision == "base_model_revision"
        assert model.lora_model_name == "lora_model_name"
        assert model.lora_model_revision == "lora_model_revision"
        assert model.lora_model_weight_name == "lora_model_weight_name"
        assert model.controlnet_model_name == "controlnet_model_name"
        assert model.controlnet_model_revision == "controlnet_model_revision"
        assert model.controlnet_model_weight_name == "controlnet_model_weight_name"
        assert model.compiled == True


def test_get_last_used_model ():
    """
    get_last_used_model

    it:
        - 前回使用したモデル情報を取得する。
        - ファイルが存在しない場合は空のDictを返す。
    """
    config = mock_config()
    model = get_last_used_model(config)
    assert model.base_model_name == "test_model"
    assert model.base_model_revision == "main"
    assert model.lora_model_name == "test_lora"
    assert model.lora_model_revision == "fp16"
    assert model.lora_model_weight_name == "test_lora_weight"
    assert model.controlnet_model_name == "test_controlnet"
    assert model.controlnet_model_revision == "fp32"
    assert model.controlnet_model_weight_name == "test_controlnet_weight"
    assert model.compiled == True

    config.STORE_LAST_USED_MODEL_DIR = Path("/not/exist/dir")
    model = get_last_used_model(config)
    assert model == {}

def test_save_last_used_model ():
    """
    save_last_used_model

    it:
        - 前回使用したモデル情報を保存する。
    """
    config = mock_config()
    config.STORE_LAST_USED_MODEL_DIR = Path(tempfile.mkdtemp())
    model = LastUsedModel(
        base_model_name="base_model_name",
        base_model_revision="base_model_revision",
        lora_model_name="lora_model_name",
        lora_model_revision="lora_model_revision",
        lora_model_weight_name="lora_model_weight_name",
        controlnet_model_name="controlnet_model_name",
        controlnet_model_revision="controlnet_model_revision",
        controlnet_model_weight_name="controlnet_model_weight_name",
        compiled=True
    )
    save_last_used_model(config, model)

    model_file = config.STORE_LAST_USED_MODEL_DIR / "model_index.json"
    assert model_file.exists()
    with open(model_file, 'r') as f:
        model_info = json.load(f)
    
    assert model_info == {
        'base': {
            'model_name': 'base_model_name',
            'revision': 'base_model_revision',
            'screen_name': ''
        },
        'lora': {
            'model_name': 'lora_model_name',
            'revision': 'lora_model_revision',
            'weight_name': 'lora_model_weight_name',
            'screen_name': ''
        },
        'controlnet': {
            'model_name': 'controlnet_model_name',
            'revision': 'controlnet_model_revision',
            'weight_name': 'controlnet_model_weight_name',
            'screen_name': ''
        },
        'compiled': True
    }