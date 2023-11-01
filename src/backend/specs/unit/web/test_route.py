""" route.pyのテスト
"""
from flask import Flask

from yt_diffuser.web.route import init_routes

class TestInitRoutes:
    """ describe: init_routes ルーティングを設定する """

    def test_init_routes (self, mocker):
        """ it: ルーティングを設定する。 """

        # 実際のルーティングはインテグレーションテストで確認する。
        mock_register_errorhandler = mocker.patch('yt_diffuser.web.api.errorhandler.register_errorhandler')

        app = Flask(__name__)
        init_routes(app)

        assert mock_register_errorhandler.call_count == 1