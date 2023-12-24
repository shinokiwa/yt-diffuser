#!/bin/sh

/usr/bin/python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel
/usr/bin/python3 -m pip install -r /workspace/src/backend/requirements.txt

/usr/bin/python3 -m yt_diffuser