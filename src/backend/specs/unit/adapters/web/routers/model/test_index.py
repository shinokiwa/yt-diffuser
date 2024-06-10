import pytest
from pytest_mock import MockerFixture

from yt_diffuser.types.enum.model import ModelSource, ModelType
from yt_diffuser.usecases.web.model import ModelUseCase

from yt_diffuser.adapters.web.routers.model.index import (
    get_model,
    ResponseDataModel
)

def test_get_model(mocker: MockerFixture):
    """
    モデル読み込みのテスト
    """
    usecase = mocker.Mock(spec=ModelUseCase)
    usecase.get_all.return_value = {
        'base_models': [
            {
                'id': 'mdl_id',
                'screen_name': 'screen_name',
                'source': ModelSource.HF,
                'model_class': ModelType.BASE_MODEL,
                'revisions': ['revisions'],
                'appends': {'appends': 'appends'}
            }
        ],
        'lora_models': [],
        'controlnet_models': []
    }

    res = get_model(usecase)

    assert usecase.get_all.called
    assert res.data.model_dump() == {
        'base_models': [
            {
                'id': 'mdl_id',
                'screen_name': 'screen_name',
                'source': ModelSource.HF,
                'model_class': ModelType.BASE_MODEL,
                'revisions': ['revisions'],
                'appends': {'appends': 'appends'}
            }
        ],
        'lora_models': [],
        'controlnet_models': []
    }
