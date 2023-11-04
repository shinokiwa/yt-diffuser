""" main.pyのテスト
"""
from multiprocessing import Pipe
from flask import Flask

from yt_diffuser.web.main import web_procedure

class TestWebProcedure:
    """ describe: web_procedure Web APIプロセスのメイン処理 """
    
    def test_web_procedure(self, mocker):
        """ it: waitressのWSGIサーバーが起動する。その際にappにAPIが登録される。
            また、shared_connにはメインプロセスから渡されたコネクションが格納される。
        """

        app = Flask(__name__)

        mock_create_app = mocker.patch('yt_diffuser.web.main.create_app', return_value=app)
        mock_set_shared_conn = mocker.patch('yt_diffuser.web.main.set_shared_conn')
        mock_start_greenlets = mocker.patch('yt_diffuser.web.main.start_listener')
        mock_serve = mocker.patch('yt_diffuser.web.main.serve')

        c, p = Pipe()
        web_procedure(shared_conn=c)

        assert mock_create_app.call_count == 1
        assert mock_set_shared_conn.call_count == 1
        assert mock_set_shared_conn.call_args[0][0] == c
        assert mock_start_greenlets.call_count == 1
        assert mock_serve.call_count == 1
        assert mock_serve.call_args[0][0] == app
        assert mock_serve.call_args[1]["host"] == '0.0.0.0'
        assert mock_serve.call_args[1]["port"] == 8000
    
    def test_web_procedure_debug(self, mocker):
        """ it: 環境変数DEBUGが1の場合はapp.debugがTrueになる。
        """
        mocker.patch.dict('os.environ', {'DEBUG': '1'})
        app = Flask(__name__)

        mocker.patch('yt_diffuser.web.main.create_app', return_value=app)
        mocker.patch('yt_diffuser.web.main.set_shared_conn')
        mocker.patch('yt_diffuser.web.main.start_listener')
        mock_serve = mocker.patch('yt_diffuser.web.main.serve')

        c, p = Pipe()
        web_procedure(shared_conn=c)

        assert mock_serve.call_args[0][0].debug == True