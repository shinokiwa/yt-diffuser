/**
 * モデルデータ管理のストア
 */
import { defineStore } from 'pinia'
import { type } from '@/domains/value/model/type'

/**
 * モデルデータを整形する
 */
export function createModelData(data) {
  return {
    id: data?.id,
    screenName: data?.screenName,
    source: data?.source,
    type: new type(data?.type),
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
     * モデルIDでモデルデータを取得する
     */
    findModelByID(id) {
      const baseModel = this.data.baseModels.find((model) => model.id === id)
      if (baseModel) {
        return baseModel
      }

      const loraModel = this.data.loraModels.find((model) => model.id === id)
      if (loraModel) {
        return loraModel
      }

      const controlnetModel = this.data.controlnetModels.find((model) => model.id === id)
      if (controlnetModel) {
        return controlnetModel
      }
      return null
    }
  }
})
