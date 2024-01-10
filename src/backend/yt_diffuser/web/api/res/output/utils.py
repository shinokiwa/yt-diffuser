"""
output API関連のユーティリティ関数群
"""
import logging; logger = logging.getLogger(__name__)
from typing import Union, Generator
import os
import json
from pathlib import Path

StrOrPath = Union[str, Path]

from yt_diffuser.utils.event import FilesystemEvent, Empty


def is_child (parent:StrOrPath, child:StrOrPath) -> bool:
    """
    childがparentの子孫かどうかを判定する。

    同一の場合もTrueとなる。
    """
    if not child.is_absolute():
        child = (parent / child).resolve()

    if isinstance(parent, str):
        parent = Path(parent)
    if isinstance(child, str):
        child = Path(child)

    return parent == child or parent in child.parents


def stream_list (path:Path, timeout:float=5.0) -> Generator[str, None, None]:
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
        
        queue = FilesystemEvent.get_listener()

        while True:
            response = ""
            try:
                data = queue.get(timeout=timeout)
                logger.debug(f"Event: {data}")
                event_path = Path(data['target'])
                if is_child(path, event_path) == False:
                    logger.debug(f"Skip event: {event_path}")
                    continue

                if not event_path.is_absolute():
                    event_path = (path / event_path).resolve()
                data['target'] = str(event_path.relative_to(path))
                data = json.dumps(data)
                
                response = f"data: {data}\n\n"
            except Empty:
                response = ": keep-alive\n\n"

            yield response
    except GeneratorExit:
        FilesystemEvent.remove_listener(queue)