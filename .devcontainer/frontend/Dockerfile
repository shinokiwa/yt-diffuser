# Vue.js開発コンテナ
FROM node:20.5.1

# ディレクトリを作成
WORKDIR /src/frontend/

COPY ./.devcontainer/frontend/entrypoint.sh /
ENTRYPOINT [ "/entrypoint.sh" ]