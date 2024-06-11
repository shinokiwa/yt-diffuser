import { type } from '@/domains/value/model/type'

/**
 * 基本モデルのエンティティ
 */
export class BaseModel {
  /**
   * コンストラクタ
   *
   * @param {Object} data モデルデータ
   */
  constructor(data) {
    /**
     * モデル名
     * @type {string}
     */
    this.id = data?.id

    /**
     * 表示名
     * @type {string}
     */
    this.screenName = data?.screenName

    /**
     * ソース
     * @type {string}
     */
    this.source = data?.source

    /**
     * モデルクラス
     * このクラスがbase-modelなので、現実的に固定値
     * @type {type}
     */
    this.type = new type(data?.type)

    /**
     * リビジョン
     * @type {array<string>}
     */
    this.revisions = []
    if (Array.isArray(data?.revisions)) {
      for (const revision of data.revisions) {
        this.revisions.push(revision)
      }
    }

    /**
     * 追加情報
     *
     * @todo いまのところ使っていないので型定義していないが、使う場合は型定義する
     * @type {Object}
     */
    this.appends = data?.appends
  }

  /**
   * 値を取得する
   *
   * @returns {Object}
   */
  getValues() {
    return {
      id: this.id,
      screenName: this.screenName,
      source: this.source,
      type: this.type.toString(),
      revisions: this.revisions,
      appends: this.appends
    }
  }
}
