/**
 * バリューオブジェクトの基底クラス
 */
export class BaseItem {
  constructor(value) {
    this.error = ''

    this._src = value
    this._value = this.validate(value)
  }

  /**
   * オブジェクトの値を取得する
   * @returns {*} value
   */
  get value() {
    return this._value
  }

  /**
   * エラーの有無を取得する
   * @returns {boolean} エラーがある場合はtrue
   */
  get hasError() {
    return this.error !== ''
  }

  /**
   * バリデーションオプションを取得する
   */
  get options() {
    return {}
  }

  /**
   * バリデーションを行う。
   * 正規化後の値を返す。正規化不能な場合はvoidになる。
   * 入力エラー時はエラーメッセージをセットする。
   *
   * @param {*} value バリデーション対象の値
   * @returns {*} 正規化された値
   */
  validate(value) {
    return value
  }

  /**
   * 値が入っていない場合だけデフォルト値を設定する
   * @param {*} value
   * @returns {*} this
   */
  default(value) {
    if (this._src === undefined) {
      this._value = value
      this._src = value
    }
    return this
  }
}
