/**
 * モデル種別のバリューオブジェクト
 */
export class type {
  static BASE_MODEL = 'base-model'
  static LORA_MODEL = 'lora-model'
  static CONTROLNET_MODEL = 'controlnet-model'

  /**
   * コンストラクタ
   *
   * @param {string} value モデルクラス (type.BASE_MODEL, type.LORA_MODEL, type.CONTROLNET_MODEL)
   */
  constructor(value) {
    /**
     * モデルクラス
     * @type {string}
     */
    this._value = value

    // 不正値の場合は全てBASE_MODELにする
    if ([type.BASE_MODEL, type.LORA_MODEL, type.CONTROLNET_MODEL].indexOf(value) === -1) {
      this._value = type.BASE_MODEL
    }
  }

  get model_class() {
    return this._value
  }

  toString() {
    return this._value
  }

  /**
   * モデルクラスがBASE_MODELかどうか
   *
   * @returns {boolean}
   */
  isBaseModel() {
    return this._value === type.BASE_MODEL
  }

  /**
   * モデルクラスがLORA_MODELかどうか
   *
   * @returns {boolean}
   */
  isLoraModel() {
    return this._value === type.LORA_MODEL
  }

  /**
   * モデルクラスがCONTROLNET_MODELかどうか
   *
   * @returns {boolean}
   */
  isControlnetModel() {
    return this._value === type.CONTROLNET_MODEL
  }
}
