""" async処理のユーティリティ
"""
import asyncio
from asyncio.tasks import Task

task:Task = None

def is_empty():
    global task
    return task is None or task.done()

def is_running():
    global task
    return task is not None and not task.done()

def run_task(procedure, args=()):
    global task
    
    if task is not None and not task.done():
        raise Exception('Task is already running')
    
    task = asyncio.create_task(procedure(*args))

def stop_task():
    global task
    
    if task is None:
        raise Exception('Task is not running')
    
    task.cancel()
    task = None