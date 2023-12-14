""" ストアの基底クラス
"""
from pathlib import Path

from yt_diffuser.config import AppConfig
from yt_diffuser.store.lock import StoreLock, StoreLockedError

class Store:
    """
    ストアの基底クラス

    ストアはディレクトリとデータベースレコードの集合体。
    どのテーブルが使われるかはサブクラスによって決まるので、
    ここではデータベースの操作は行わない。
    """

    def __init__(self, config: AppConfig, store_name: str) -> None:
        """
        コンストラクタ
        渡されたConfigからストアディレクトリのパスを生成する。

        args:
            config: アプリケーション設定値
            path: ベースディレクトリからの相対パス
        """
        self.config:AppConfig = config
        self.store_name: str = store_name
    
    @property
    def path(self) -> Path:
        """
        ストアディレクトリのパスを返す。

        returns:
            Path: パス
        """
        return self.config.STORE_DIR / self.store_name

    def exists(self) -> bool:
        """
        ストアディレクトリが存在するかどうかを返す。

        returns:
            bool: ストアディレクトリが存在する場合はTrue
        """
        return self.path.exists()
    
    def mkdir(self) -> None:
        """
        ストアディレクトリを作成する。

        ストアディレクトリが存在していてもエラーにはならないが、
        ロックされているときは StoreLockedError が送出される。

        raises:
            StoreLockedError: ストアディレクトリがロックされている場合
        """
        if StoreLock(self.path).is_locked():
            raise StoreLockedError(self.path)

        self.path.mkdir(parents=True, exist_ok=True)
