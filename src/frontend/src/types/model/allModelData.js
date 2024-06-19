import { BaseModelData } from './index'

/**
 * 全モデルのリストデータ
 */
export class AllModelData {
  constructor(data) {
    this.baseModels = []
    this.loraModels = []
    this.controlnetModels = []

    if (data) {
      this.setData(data)
    }
  }

  /**
   * データをセットする
   */
  setData(data) {
    this.baseModels.splice(0, this.baseModels.length)
    this.loraModels.splice(0, this.loraModels.length)
    this.controlnetModels.splice(0, this.controlnetModels.length)

    if (Array.isArray(data.baseModels)) {
      data.baseModels.forEach((model) => {
        this.baseModels.push(new BaseModelData(model))
      })
    }

    if (Array.isArray(data.loraModels)) {
      data.loraModels.forEach((model) => {
        this.data.loraModels.push(new BaseModelData(model))
      })
    }

    if (Array.isArray(data.controlnetModels)) {
      data.controlnetModels.forEach((model) => {
        this.data.controlnetModels.push(new BaseModelData(model))
      })
    }
  }
}
