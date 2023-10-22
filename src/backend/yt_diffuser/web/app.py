""" Flaskのアプリ定義
"""
from flask import Flask
from multiprocessing.connection import Connection

from .api import regist_api

app = Flask(__name__)
""" Flaskのインスタンス
"""

shared_conn:Connection = None
""" データ処理プロセスとの共有コネクション
"""

@app.route('/send_message/<message>')
def send_message(message):
    #queue.put(message)
    return f'Sent message: {message}'

regist_api(app)