import pytest
from pytest_mock import MockerFixture

from yt_diffuser.usecases.web.model import ModelLoadUseCase

from yt_diffuser.adapters.web.routers.model.load import (
    RequestData, load_model
)

def test_load_model(mocker: MockerFixture):
    """
    モデル読み込みのテスト
    """
    mock_usecase = mocker.Mock(spec=ModelLoadUseCase)

    data = RequestData(base_model_name='test', base_revision='1', compile=False)

    res = load_model(data, mock_usecase)

    assert res.data == 'success'
    assert mock_usecase.load.call_count == 1
