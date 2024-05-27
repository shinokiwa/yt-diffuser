/**
 * 文字列型 バリューオブジェクト
 */
import { BaseItem } from './baseItem'

export class StringItem extends BaseItem {
  get options() {
    return {
      label: '文字列',
      minLength: 0,
      maxLength: 0
    }
  }

  /**
   * バリデーションを行う
   *
   * @param {*} value
   * @returns {*} 正規化された値
   */
  validate(value) {
    const val = String(value || '')
    if (this.options.minLength > 0 && val.length === 0) {
      this.error = `${this.options.label}を入力してください。`
      return
    }

    if (val.length < this.options.minLength) {
      this.error = `${this.options.label}は${this.options.minLength}文字以上で入力してください。`
      return
    }

    if (this.options.maxLength > 0 && val.length > this.options.maxLength) {
      this.error = `${this.options.label}は${this.options.maxLength}文字以内で入力してください。`
      return
    }

    return val
  }
}
