/**
 * モデルデータ管理のストア
 */
import { defineStore } from 'pinia'
import { toRef } from 'vue'

/**
 * モデルデータ管理のストアを返す
 */
export const useModelStore = defineStore('model', {
  state: () => ({
    /**
     * モデルデータ
     */
    data: {
      baseModels: [],
      loraModels: [],
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
        this.data.baseModels = data.baseModels
      }
      if (Array.isArray(data.loraModels)) {
        this.data.loraModels = data.loraModels
      }
      if (Array.isArray(data.controlnetModels)) {
        this.data.controlnetModels = data.controlnetModels
      }
    }
  }
})
