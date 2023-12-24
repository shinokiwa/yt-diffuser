# Vue.js開発コンテナ
FROM node:20.10.0

# ディレクトリを作成
WORKDIR /src/frontend/

COPY ./.devcontainer/frontend/entrypoint.sh /
ENTRYPOINT [ "/entrypoint.sh" ]