"""
yt_diffuser.store.model のテスト
"""
import pytest

from yt_diffuser.store.model import *

class TestModelInfo:
    """
    ModelInfo のテスト
    """

    def test_init (self):
        """
        初期化テスト
        """
        model_info = ModelInfo(
            model_name="model_name",
            model_class=ModelClass.BASE_MODEL,
            source=ModelSource.HUB,
        )

        assert model_info.model_name == "model_name"
        assert model_info.model_class == ModelClass.BASE_MODEL
        assert model_info.source == ModelSource.HUB
        assert model_info.revisions == []
        assert model_info.screen_name == None
        assert model_info.appends == {"pipeline_name": "", "precision": ""}


        model_info = ModelInfo(
            model_name="model_name",
            model_class=ModelClass.LORA_MODEL,
            source=ModelSource.HUB
        )

        assert model_info.model_name == "model_name"
        assert model_info.model_class == ModelClass.LORA_MODEL
        assert model_info.source == ModelSource.HUB
        assert model_info.revisions == []
        assert model_info.screen_name == None
        assert model_info.appends == {"weight_name": ""}

        with pytest.raises(ValueError):
            model_info = ModelInfo(
                model_name="model_name",
                model_class="invalid",
                source=ModelSource.HUB
            )


    def test_add_revision (self):
        """
        リビジョン追加テスト
        """
        model_info = ModelInfo(
            model_name="model_name",
            model_class=ModelClass.LORA_MODEL,
            source=ModelSource.HUB,
        )

        model_info.add_revision("revision3")
        assert model_info.revions == ["revision3"]

    def test_set_screen_name (self):
        """
        スクリーン名設定テスト
        """
        model_info = ModelInfo(
            model_name="model_name",
            model_class=ModelClass.LORA_MODEL,
            source=ModelSource.HUB,
        )

        model_info.set_screen_name("screen_name")
        assert model_info.screen_name == "screen_name"

    def test_set_append (self):
        """
        付加情報設定テスト
        """
        model_info = ModelInfo(
            model_name="model_name",
            model_class=ModelClass.LORA_MODEL,
            source=ModelSource.HUB,
        )

        model_info.set_append("key", "value")
        assert model_info.appends == {
            "weight_name": "",
            "key": "value"
        }

    def test_to_dict (self):
        """
        辞書変換テスト
        """
        model_info = ModelInfo(
            model_name="model_name",
            model_class=ModelClass.LORA_MODEL,
            source=ModelSource.HUB,
        )

        model_info.add_revision("revision1")
        model_info.add_revision("revision2")

        assert model_info.to_dict() == {
            'model_name': "model_name",
            'model_class': ModelClass.LORA_MODEL.value,
            'source': ModelSource.HUB.value,
            'revisions': ["revision1", "revision2"],
            'screen_name': None,
            'appends': {"weight_name": ""},
        }
