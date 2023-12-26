"""
output API関連のユーティリティ関数群
"""
from typing import Union, Generator
import os
import json
from pathlib import Path

StrOrPath = Union[str, Path]

from yt_diffuser.web.message_listener import get_event_listener, remove_event_listener, Empty
from yt_diffuser.utils.message_queue import EVENT_TYPE_FILESYSTEM


def is_child (parent:StrOrPath, child:StrOrPath) -> bool:
    """
    childがparentの子孫かどうかを判定する。

    同一の場合もTrueとなる。
    """
    if isinstance(parent, str):
        parent = Path(parent)
    if isinstance(child, str):
        child = Path(child)

    return parent == child or parent in child.parents


def stream_list (path:Path, timeout:float=20.0) -> Generator[str, None, None]:
    """
    ファイル一覧をstreamで返し、その後はFILESYSTEMイベントを受け取って返す。

    - ファイル一覧は指定したパスからの相対パスで返す。
    """
    queue = None
    try:
        data = {'type': 'list', 'target': None}
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                full_path = Path(dirpath) / filename
                data['target'] = str(full_path.relative_to(path))
                _data = json.dumps(data)
                yield f"data: {_data}\n\n"            
        
        queue = get_event_listener('file')

        while True:
            try:
                data = queue.get(timeout=timeout)
                if type(data) == dict:
                    event_path = Path(data['target'])
                    if is_child(path, event_path) == False:
                        continue

                    data['target'] = str(event_path.relative_to(path))
                    data = json.dumps(data)
            except Empty:
                data = ""

            yield f"data: {data}\n\n"            
    except GeneratorExit:
        remove_event_listener(EVENT_TYPE_FILESYSTEM, queue)