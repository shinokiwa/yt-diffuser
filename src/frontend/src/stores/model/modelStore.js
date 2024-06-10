/**
 * モデルデータ管理のストア
 */
import { defineStore } from 'pinia'
import { ModelClass } from '@/domains/value/model/modelClass'

/**
 * モデルデータを整形する
 */
export function createModelData(data) {
  return {
    modelName: data?.modelName,
    screenName: data?.screenName,
    source: data?.source,
    modelClass: new ModelClass(data?.modelClass),
    revisions: data?.revisions || [],
    appends: data?.appends
  }
}

/**
 * モデルデータ管理のストアを返す
 */
export const useModelStore = defineStore('model', {
  state: () => ({
    /**
     * モデルデータ
     */
    data: {
      /**
       * @type {ReturnType<typeof createModelData>[]}
       */
      baseModels: [],
      /**
       * @type {ReturnType<typeof createModelData>[]}
       */
      loraModels: [],
      /**
       * @type {ReturnType<typeof createModelData>[]}
       */
      controlnetModels: []
    }
  }),
  actions: {
    /**
     * モデルデータをセットする
     *
     * @param {Object} data モデルデータ
     */
    setData(data) {
      if (Array.isArray(data.baseModels)) {
        this.data.baseModels = []
        data.baseModels.forEach((model) => {
          this.data.baseModels.push(createModelData(model))
        })
      }
      if (Array.isArray(data.loraModels)) {
        this.data.loraModels = []
        data.loraModels.forEach((model) => {
          this.data.loraModels.push(createModelData(model))
        })
      }
      if (Array.isArray(data.controlnetModels)) {
        this.data.controlnetModels = []
        data.controlnetModels.forEach((model) => {
          this.data.controlnetModels.push(createModelData(model))
        })
      }
    },

    /**
     * モデル名でモデルデータを取得する
     */
    findModelByName(modelName) {
      const baseModel = this.data.baseModels.find((model) => model.modelName === modelName)
      if (baseModel) {
        return baseModel
      }

      const loraModel = this.data.loraModels.find((model) => model.modelName === modelName)
      if (loraModel) {
        return loraModel
      }

      const controlnetModel = this.data.controlnetModels.find(
        (model) => model.modelName === modelName
      )
      if (controlnetModel) {
        return controlnetModel
      }
      return null
    }
  }
})
