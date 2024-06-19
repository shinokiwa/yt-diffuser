import { defineStore } from 'pinia'
import { AllModelData } from '@/types/model/'

/**
 * モデルデータ管理のストアを返す
 */
export const useModelStore = defineStore('model', {
  state: () => ({
    /**
     * モデルデータ
     *
     * @type {AllModelData}
     */
    data: new AllModelData()
  }),
  actions: {
    /**
     * モデルデータをセットする
     *
     * @param {AllModel | Object} data モデルデータ
     */
    setData(data) {
      this.data.setData(data)
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
