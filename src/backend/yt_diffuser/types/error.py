class NoProcessError(Exception):
    """
    プロセスが存在しないエラー

    プロセス起動前にプロセス処理を行おうとした場合に発生する例外
    """
    pass

class DuplicateProcessError(Exception):
    """
    重複プロセスエラー

    既に同じプロセスが実行中の場合に発生する例外
    """
    pass

class GeneratorExitSignal(Exception):
    """
    終了シグナル

    raiseで処理するのでExceptionを継承
    """
    pass

class ErrorMessageSignal(Exception):
    """
    エラーメッセージシグナル


    """
    pass