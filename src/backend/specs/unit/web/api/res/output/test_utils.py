"""
yt_diffuser.web.api.res.output.utils のテスト
"""
import pytest
from pathlib import Path

from yt_diffuser.web.api.res.output.utils import *

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

def test_stream_list (mocker):
    """
    stream_list
    
    it:
        - ファイル一覧をstreamで返す。
        - FILESYSTEMイベントを受け取って返す。
    """ 
    mock_walk = mocker.patch('yt_diffuser.web.api.res.output.utils.os.walk')
    mock_get_event_listener = mocker.patch('yt_diffuser.web.api.res.output.utils.get_event_listener')
    
    mock_walk.return_value = [
        ('/path/to/dir', ['subdir'], ['file1', 'file2']),
        ('/path/to/dir/subdir', [], ['file3', 'file4'])
    ]

    mock_get_event_listener.return_value.get.side_effect = [
        "",
        Empty,
        {'type': 'test', 'target': '/path/to/dir/subdir2/file5'},
        {'type': 'test', 'target': '/path/dir/file6'},
        GeneratorExit
    ]

    path = Path('/path/to/dir')
    result = list(stream_list(path))

    assert result == [
        "data: {\"type\": \"list\", \"target\": \"file1\"}\n\n",
        "data: {\"type\": \"list\", \"target\": \"file2\"}\n\n",
        "data: {\"type\": \"list\", \"target\": \"subdir/file3\"}\n\n",
        "data: {\"type\": \"list\", \"target\": \"subdir/file4\"}\n\n",
        "data: \n\n",
        "data: \n\n",
        "data: {\"type\": \"test\", \"target\": \"subdir2/file5\"}\n\n",
    ]
