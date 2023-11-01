""" app.pyのテスト
"""
from flask import Flask

from yt_diffuser.web.app import create_app

class TestCreateApp:
    """ describe: create_app Flaskのインスタンスを作成する """

    def test_create_app (self, mocker):
        """ it: Flaskのインスタンスを作成する。 """

        mock_init_routes = mocker.patch('yt_diffuser.web.app.init_routes')
        app = create_app()

        assert type(app) == Flask
        assert mock_init_routes.call_count == 1