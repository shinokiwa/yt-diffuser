# ディレクトリ構成

ディレクトリ構成について記載。

## 構成

### .devcontainer

VSCodeのDev Containers向け各種定義ファイル

### .vscode

VSCode向け設定ファイル

### data

各種データを保存するディレクトリ。リポジトリには含まれず、自動作成される。

- db : データベースディレクトリ
- store : AI関係のデータディレクトリ
  - models : 学習済みモデルファイル
    - huggingface : HuggingFace Hub からダウンロードしたモデル
      - ※これ以下はHuggingFace Hub Clientのキャッシュシステムによって生成される
      - models--{namespace}--{repo_id} : モデルのディレクトリ
        - blobs : モデルのファイル実体
        - refs : ブランチなどに対応するコミットハッシュの参照
        - snapshots : スナップショット
            - {commit_hash} : コミットハッシュごとのスナップショット(実際はblobsへのシンボリックリンク)
    - local : ローカルで学習したモデル

    - images : 画像ファイル
      - temp : 一時的な画像ファイル(生成直後はここに入る)
      - gallery : ギャラリー用ファイル
      - editor : エディター用ファイル

### docs

汎用的なドキュメントを格納するディレクトリ。

### src

ソースコードディレクトリ。

- backend : バックエンドのソースコード
  - specs : バックエンド用テストコード
    - feature : 機能テスト用コード
    - unit : ユニットテスト用コード
  - yt_diffuser : バックエンドモジュール本体
- frontend : フロントエンドのソースコード
  - public : 静的ファイル
  - specs : フロントエンド用テストコード
  - src : フロントエンドのソースコード