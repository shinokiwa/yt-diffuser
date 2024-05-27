#################################
## DevContainer構成用Dockerfile
#################################

# NVIDIA CUDA 12.1 Ubuntu用をベースイメージにする
FROM nvidia/cuda:12.1.0-base-ubuntu22.04 AS base

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    language-pack-ja \
    build-essential \
    git curl \
    python3-pip python3-venv \
    python3.10-dev \
    libgl1-mesa-glx libglib2.0-0

# DockerオフィシャルのGPGキーを追加
RUN install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc && \
    chmod a+r /etc/apt/keyrings/docker.asc

# Dockerのリポジトリを追加
RUN echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    tee /etc/apt/sources.list.d/docker.list > /dev/null
RUN apt-get update && apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Node.jsインストール
RUN curl -sL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs

WORKDIR /workspace/src/

# ENTRYPOINTを設定
COPY ./.devcontainer/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT [ "/usr/local/bin/entrypoint.sh" ]