""" データ処理プロセスのメイン処理
"""

def processing_process(shared_conn, parent_conn):
    print('Processing process started...')
    while True:
        message = shared_conn.recv()
        if message == 'exit':
            print('Exiting processing process.')
            break
        print(f'Received message: {message}')
        # ここで重いデータ処理や機械学習タスクを実行する
