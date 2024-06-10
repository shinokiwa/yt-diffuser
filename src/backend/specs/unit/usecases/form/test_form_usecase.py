import pytest
from pytest_mock import MockerFixture

from yt_diffuser.stores.database.store.store import IDBStore

from yt_diffuser.usecases.web.form.form_usecase import (
    FormUseCase,
    IDBConnection,
    IDBStore
)

class TestFormUseCase:
    """
    FormUseCase

    最新のフォーム情報を管理するユースケース
    """

    def test_read(self, mocker: MockerFixture):
        """
        read

        it:
            - フォーム情報を取得する
        """
        conn = mocker.MagicMock(spec=IDBConnection)
        store = mocker.MagicMock(spec=IDBStore)
        store.read.return_value = b'{"test": "value"}'

        form = FormUseCase(conn, store)

        result = form.read()

        assert result == {"test": "value"}, "フォーム情報を取得する。"

        assert conn.__enter__.call_count == 1, "DBコネクションを開く"
        assert store.read.call_args.args[0] == "api/form"
        assert store.read.call_args.args[1] == b"{}"


    def test_write(self, mocker: MockerFixture):
        """
        write

        it:
            - フォーム情報を保存する
        """
        conn = mocker.MagicMock(spec=IDBConnection)
        store = mocker.MagicMock(spec=IDBStore)

        form = FormUseCase(conn, store)

        form.write({"test": "value"})

        assert conn.__enter__.call_count == 1, "DBコネクションを開く"
        assert store.write.call_args.args[0] == "api/form"
        assert store.write.call_args.args[1] == '{"test": "value"}'