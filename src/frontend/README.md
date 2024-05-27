# ゆとりでふーざー フロントエンド

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

### Run Unit Tests with [Vitest](https://vitest.dev/)

```sh
npm run test:unit
```

### Run End-to-End Tests with [Cypress](https://www.cypress.io/)

```sh
npm run test:e2e:dev
```

This runs the end-to-end tests against the Vite development server.
It is much faster than the production build.

But it's still recommended to test the production build with `test:e2e` before deploying (e.g. in CI environments):

```sh
npm run build
npm run test:e2e
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```

## ディレクトリ構成とアーキテクチャ

基本的には Vue.js の構成を Clean Architecture に沿って構築している。<br>
ディレクトリはトップレベルディレクトリのみ複数形、配下ディレクトリは単数形で命名している。<br>
ソースコードの各ディレクトリには、ユニットテストとして `__specs__` ディレクトリを配置している。<br>
また、必要に応じてモックのデータを `__mocks__` ディレクトリに配置している。

- src : アプリケーションのエントリーポイント
  - assets : 画像やフォントなどの静的ファイル

  - composables : Vue コンポーザブルを UseCase として配置。
  - stores : Pinia ストアを Repository として配置。

  - drivers : ドライバ層を配置。
    - api : API 通信
  
  - components : Vue コンポーネントを配置。 composition API を Controller & Presenter として使用。
