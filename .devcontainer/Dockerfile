# Baseステージは本番用とDevContainer用で共通

# NVIDIA CUDA 12.1 Ubuntu用をベースイメージにする
FROM nvidia/cuda:12.1.0-base-ubuntu22.04 AS base

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    language-pack-ja \
    build-essential \
    git curl \
    python3-pip python3-venv \
    python3.10-dev \
    libgl1-mesa-glx libglib2.0-0 \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Node.jsインストール
RUN curl -sL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# PyTorchインストール
WORKDIR /workspace/src/backend/
RUN python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel
COPY ./src/backend/requirements-torch.txt /workspace/src/backend/
RUN python3 -m pip install -r /workspace/src/backend/requirements-torch.txt


#################################
# DevContainer用のイメージを構成
FROM base AS devcontainer

# pipインストール
WORKDIR /workspace/src/backend/
COPY ./src/backend/requirements.txt /workspace/src/backend/
RUN python3 -m pip install -r /workspace/src/backend/requirements.txt
COPY ./src/backend/requirements-dev.txt /workspace/src/backend/
RUN python3 -m pip install -r /workspace/src/backend/requirements-dev.txt

# npmインストール
WORKDIR /workspace/src/frontend
COPY ./src/frontend/package.json /workspace/src/frontend/
RUN npm install

# Nginxの設定
COPY ./.devcontainer/nginx.conf /etc/nginx/nginx.conf

# ワークスペースの設定
WORKDIR /workspace/src/

COPY ./.devcontainer/server_start.sh /
COPY ./.devcontainer/entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]