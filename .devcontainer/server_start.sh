#!/bin/bash
echo 'Starting yt_diffuser server...'

# スクリプト終了時に実行する関数を定義
cleanup() {
    cd "$original_dir"
    echo "スクリプト終了時に元のディレクトリに戻りました。"
}

# 現在のディレクトリを保存
original_dir=$(pwd)

# トラップを設定
trap cleanup EXIT

# ログディレクトリの作成
mkdir -p /var/log/yt_diffuser

# バックグラウンドサーバー起動
if ps aux | grep -v grep | grep -q '/usr/bin/python3 -m yt_diffuser'; then
    echo "バックエンドサービスは既に起動しています。"
else
    cd /workspace/src/backend
    /usr/bin/python3 -m yt_diffuser > /var/log/yt_diffuser/backend.log 2>&1 &
fi

# フロントエンドサーバー起動
if ps aux | grep -v grep | grep -q '/usr/bin/npm run dev'; then
    echo "フロントエンドサービスは既に起動しています。"
else
    cd /workspace/src/frontend
    /usr/bin/npm run dev > /var/log/yt_diffuser/frontend.log 2>&1 &
fi

# Nginx起動
if ps aux | grep -v grep | grep -q '/usr/sbin/nginx'; then
    echo "Nginxは既に起動しています。"
else
    /usr/sbin/nginx -g 'daemon off;' > /var/log/yt_diffuser/nginx.log 2>&1 &
fi
