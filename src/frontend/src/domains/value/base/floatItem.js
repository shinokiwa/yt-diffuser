/**
 * 浮動小数点型 バリューオブジェクト
 */
import { IntItem } from './intItem'

export class FloatItem extends IntItem {
  /**
   * バリデーションを行う
   *
   * @param {*} value
   * @returns {*} 正規化された値
   */
  validate(value) {
    const val = parseFloat(value || 0)

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
