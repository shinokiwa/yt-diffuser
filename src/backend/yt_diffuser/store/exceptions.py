"""
ストアに関する例外
"""

class StoreExistsError(Exception):
    """
    ストアが既に存在する場合の例外
    """
    pass

class StoreNotFoundError(Exception):
    """
    ストアが存在しない場合の例外
    """
    pass

class StoreLockedError(Exception):
    """
    ストアがロックされている場合の例外
    """
    pass