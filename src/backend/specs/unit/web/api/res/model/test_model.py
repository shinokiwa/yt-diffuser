""" modelモジュールのテスト """

from flask import Blueprint

from yt_diffuser.web.api.res.model import model_bp, get_model

class TestModelBp:
    """ describe: model_bp Blueprintオブジェクト"""

    def test_model_bp(self):
        """ it: model_bpはBlueprintオブジェクト """

        assert type(model_bp) == Blueprint

class TestGetModel:
    """ describe: get_model 保存済みのモデル一覧を取得する """

    def test_get_model (self):
        """ it: get_modelは保存済みのモデル一覧を取得する。 """

        data = get_model()

        assert data['models'] == []
