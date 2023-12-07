""" download.py のテスト
"""
import pytest
import asyncio
import tempfile
from multiprocessing import Queue

from yt_diffuser.config import AppConfig
from yt_diffuser.worker.procs.download import download_procedure

@pytest.mark.describe('ダウンロードのプロシージャ')
@pytest.mark.it('ダウンロード処理を開始する。')
@pytest.mark.asyncio
async def test_download_procedure():
    config = AppConfig(base_dir=tempfile.mkdtemp())
    queue = Queue()

    p = asyncio.create_task(download_procedure(config, queue, 'download', None))
    
    while queue.empty():
        await asyncio.sleep(0.1)
    r = queue.get(timeout=1)
    assert r[0] == 'download'
    assert r[1].keys() == {'elapsed', 'percentage', 'progress', 'remaining', 'target', 'total'}
    assert r[1]['target'] == 'CompVis/stable-diffusion-v1-4/fp16'
    assert r[1]['total'] == 0
    assert r[1]['progress'] == 0


    while queue.empty():
        await asyncio.sleep(0.1)
    r = queue.get(timeout=1)
    assert r[0] == 'download'
    assert r[1].keys() == {'elapsed', 'percentage', 'progress', 'remaining', 'target', 'total'}
    assert r[1]['target'] == 'CompVis/stable-diffusion-v1-4/fp16'
    assert r[1]['total'] == 10
    assert r[1]['progress'] == 0

    while queue.empty():
        await asyncio.sleep(0.1)
    assert queue.get(timeout=1)[1]['progress'] == 1

    while queue.empty():
        await asyncio.sleep(0.1)
    assert queue.get(timeout=1)[1]['progress'] == 2

    while queue.empty():
        await asyncio.sleep(0.1)
    assert queue.get(timeout=1)[1]['progress'] == 3

    while queue.empty():
        await asyncio.sleep(0.1)
    assert queue.get(timeout=1)[1]['progress'] == 4

    while queue.empty():
        await asyncio.sleep(0.1)
    assert queue.get(timeout=1)[1]['progress'] == 5

    while queue.empty():
        await asyncio.sleep(0.1)
    assert queue.get(timeout=1)[1]['progress'] == 6

    while queue.empty():
        await asyncio.sleep(0.1)
    assert queue.get(timeout=1)[1]['progress'] == 7

    while queue.empty():
        await asyncio.sleep(0.1)
    assert queue.get(timeout=1)[1]['progress'] == 8

    while queue.empty():
        await asyncio.sleep(0.1)
    assert queue.get(timeout=1)[1]['progress'] == 9

    while queue.empty():
        await asyncio.sleep(0.1)
    assert queue.get(timeout=1)[1]['progress'] == 10
    await p