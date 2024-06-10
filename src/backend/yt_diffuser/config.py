""" アプリケーション設定値
"""

class AppConfig:
    """ アプリケーション設定値
    """

    def __init__(self,
                 debug:bool=False,
                 offline:bool=False
                 ) -> None:
        """
        コンストラクタ

        一部の設定値は引数によりオーバーライド可能。

        Args:
            debug: デバッグモード
            offline: オフラインモード
        """

        self.debug: bool = debug
        """
        デバッグモード
        """

        self.offline: bool = offline
        """
        オフラインモード
        主にテスト用で、ネットワークからモデルをダウンロードしない。
        """
