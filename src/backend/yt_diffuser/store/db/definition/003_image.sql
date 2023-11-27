-- 画像情報マスター

CREATE TABLE image (
    id              INTEGER     NOT NULL    PRIMARY KEY AUTOINCREMENT,  -- ID
    path            TEXT        NOT NULL,                               -- パス
    last_modified   DATETIME    NOT NULL,                               -- 最終更新日時
    updated_at      DATETIME    NOT NULL    DEFAULT CURRENT_TIMESTAMP,  -- 更新日時
    registed_at     DATETIME    NOT NULL    DEFAULT CURRENT_TIMESTAMP   -- 登録日時
);

-- インデックス
CREATE UNIQUE INDEX image_path ON image (path);
