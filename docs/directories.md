# ディレクトリ構成

ディレクトリ構成について記載。

## 構成

- .devcontainer : VSCodeのDev Containers向け各種定義ファイル
- .vscode : VSCode向け設定ファイル

- data : データディレクトリ、リポジトリには含まれない
  - db : データベースファイル
  - store : 各種データファイル
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
      - gallery : ギャラリー用ファイル
      - editor : エディター用ファイル

- docs : 汎用的なドキュメント

- src : ソースコード
  - backend : バックエンドのソースコード
    - specs : バックエンド用テストコード
      - feature : 機能テスト用コード
      - unit : ユニットテスト用コード
    - yt_diffuser : バックエンドモジュール本体
  - frontend : フロントエンドのソースコード
    - public : 静的ファイル
    - specs : フロントエンド用テストコード
    - src : フロントエンドのソースコード