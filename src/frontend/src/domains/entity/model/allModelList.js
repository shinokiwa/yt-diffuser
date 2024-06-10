import { BaseModel } from '@/domains/entity/model/baseModel'
import { ModelClass } from '@/domains/value/model/modelClass'

/**
 * 全モデルリストのエンティティ
 */
export class AllModelList {
  /**
   * コンストラクタ
   *
   * @param {Object} data モデルデータ
   */
  constructor(data) {
    this.baseModels = []
    this.loraModels = []
    this.controlnetModels = []

    if (Array.isArray(data?.baseModels)) {
      data.baseModels.forEach((v) => {
        this.baseModels.push(new BaseModel(v))
      })
    }

    if (Array.isArray(data?.loraModels)) {
      data.loraModels.forEach((v) => {
        this.loraModels.push(new BaseModel(v))
      })
    }

    if (Array.isArray(data?.controlnetModels)) {
      data.controlnetModels.forEach((v) => {
        this.controlnetModels.push(new BaseModel(v))
      })
    }
  }

  /**
   * 値を取得する
   *
   * @returns {Object}
   */
  getValues() {
    return {
      baseModels: this.baseModels.map((v) => v.getValues()),
      loraModels: this.loraModels.map((v) => v.getValues()),
      controlnetModels: this.controlnetModels.map((v) => v.getValues())
    }
  }
}
