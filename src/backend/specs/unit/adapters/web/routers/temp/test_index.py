import pytest
from pytest_mock import MockerFixture

from yt_diffuser.adapters.web.routers.temp.index import get_temp_index , ResponseModel, ResponseData, ResponseMeta

def test_get_temp_index(mocker: MockerFixture):
    """
    get_temp_index

    it:
        - 一時保存画像の一覧を取得する
    """
    usecase = mocker.MagicMock()
    usecase.get_index.return_value = ['test1.jpg', 'test2.jpg', 'test3.jpg']

    result = get_temp_index(usecase)

    assert result == ResponseModel[ResponseData](
        data=ResponseData(list=['test1.jpg', 'test2.jpg', 'test3.jpg'])
    ), "一時保存画像の一覧を取得する。"