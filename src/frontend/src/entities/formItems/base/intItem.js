/**
 * 整数型 バリューオブジェクト
 */
import { BaseItem } from './baseItem'

export class IntItem extends BaseItem {
  /**
   * バリデーションオプションを取得する
   *
   * @returns {object} バリデーションオプション
   * @returns {string} バリデーションオプション.label ラベル
   * @returns {number} バリデーションオプション.min 最小値 NaNの場合は制限なし
   * @returns {number} バリデーションオプション.max 最大値 NaNの場合は制限なし
   */
  get options() {
    return {
      label: '数値',
      min: NaN,
      max: NaN
    }
  }

  /**
   * バリデーションを行う
   *
   * @param {*} value
   * @returns {*} 正規化された値
   */
  validate(value) {
    const val = parseInt(value || 0, 10)

    if (isNaN(this.options.min) === false && val < this.options.min) {
      this.error = `${this.options.label}は${this.options.min}以上で入力してください。`
      return
    }

    if (isNaN(this.options.max) === false && val > this.options.max) {
      this.error = `${this.options.label}は${this.options.max}以下で入力してください。`
      return
    }

    return val
  }
}
