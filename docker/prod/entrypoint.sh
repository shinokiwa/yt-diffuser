#!/bin/bash

# バックグラウンドサーバー起動
cd /workspace/src/backend
/usr/bin/python3 -m yt_diffuser 2>&1 &

# Nginx起動
/usr/sbin/nginx -g 'daemon off;'
