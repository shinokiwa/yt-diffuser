/**
 * 真偽値型 バリューオブジェクト
 */
import { BaseItem } from './baseItem'

export class BoolItem extends BaseItem {
  get options() {
    return {
      label: '真偽値'
    }
  }

  /**
   * バリデーションを行う
   *
   * エラーパターンはない
   *
   * @param {*} value
   * @returns {*} 正規化された値
   */
  validate(value) {
    const val = Boolean(value || false)
    return val
  }
}
