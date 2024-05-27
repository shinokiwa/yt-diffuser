import { ValidateResult } from '@/entities/validateResult'

/**
 * エディターの基本フォーム
 */
export class EditorBasicForm {
  constructor(data) {
    this.seed = data?.seed || 0
    this.generateType = data?.generateType || 't2i'
    this.width = data?.width || 1024
    this.height = data?.height || 1024
    this.strength = data?.strength || 0.3
  }

  /**
   * バリデーション
   *
   * @returns {ValidateResult} バリデーション結果
   */
  validate() {
    const errors = {}
    const validData = {}
    let isValid = true

    if (this.width < 1) {
      errors.width = '1以上の値を入力してください'
      isValid = false
    }

    if (this.height < 1) {
      errors.height = '1以上の値を入力してください'
      isValid = false
    }

    if (this.strength < 0 || this.strength > 1) {
      errors.strength = '0以上1以下の値を入力してください'
      isValid = false
    }

    return new ValidateResult(isValid, validData, errors)
  }
}
