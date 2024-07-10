import pytest
from pathlib import Path

from yt_diffuser.utils.file_path import *

def test_is_child ():
    """
    is_child

    it:
        - childがparentの子孫であればTrueを返す。
        - childがparentと同一であればTrueを返す。
        - childがparentの子孫でなければFalseを返す。
    """
    parent = Path('/path/to/parent')
    child = Path('/path/to/parent/child')

    assert is_child(parent, child) == True
    assert is_child(parent, parent) == True
    assert is_child(child, parent) == False

    parent = '/path/to/parent'
    child = '/path/to/parent/child'

    assert is_child(parent, child) == True
    assert is_child(parent, parent) == True
    assert is_child(child, parent) == False