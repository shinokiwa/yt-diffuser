import pytest
from pytest_mock import MockerFixture

from logging import getLogger; logger = getLogger(__name__)

from yt_diffuser.usecases.web.form.form_usecase import FormUseCase

from yt_diffuser.adapters.web.routers.form.index import get_form

def test_get_form(mocker:MockerFixture):
    """
    get_formのテスト
    """
    usecase = mocker.MagicMock(FormUseCase)
    usecase.read.return_value = {
        'key': 'value'
    }

    response = get_form(usecase)

    assert response.data == {
        'key': 'value'
    }

    assert usecase.read.called