""" マルチプロセス処理の例外定義
"""

class DuplicateProcessError(Exception):
    """ 重複プロセスエラー

    既に同じプロセスが実行中の場合に発生する例外
    """
    pass