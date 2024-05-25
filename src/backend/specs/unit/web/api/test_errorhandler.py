""" errorhandler.pyのテスト """

from werkzeug.exceptions import HTTPException
from flask import jsonify, Flask, Blueprint

from yt_diffuser.web.api.errorhandler import handle_http_exception, register_errorhandler

class TestHandleHttpException:
    """ describe: handle_http_exception 例外ハンドラ """

    def test_handle_http_exception (self):
        """ it: handle_http_exceptionはHTTPExceptionをハンドルする。 """

        app = Flask(__name__)

        with app.test_request_context():
            e = HTTPException('test error')
            e.code = 500
            response = handle_http_exception(e)
            assert response[0].json == jsonify({'error': 'test error'}).json
            assert response[1] == 500


class TestRegisterErrorhandler:
    """ describe: register_errorhandler エラーハンドラ """

    def test_register_errorhandler (self):
        """ it: register_errorhandlerはエラーハンドラを登録する。 """

        bp = Blueprint('test', __name__)
        register_errorhandler(bp)

        assert len(bp.error_handler_spec[None]) == 1
        assert bp.error_handler_spec[None][None][HTTPException] == handle_http_exception