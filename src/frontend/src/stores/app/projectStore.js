import { defineStore } from 'pinia'
import { Project } from '@/types/project'

/**
 * プロジェクトデータ管理のストアを返す
 */
export const useProjectStore = defineStore('project', {
  state: () => ({
    /**
     * 読み込み予約のプロジェクト名
     */
    defferedName: '',

    /**
     * 現在開いているプロジェクト
     */
    data: new Project(),

    /**
     * 選択中のレイヤーID
     */
    selectedLayer: null
  }),
  getters: {
    isOpen() {
      return this.data.projectName !== ''
    }
  },

  actions: {
    /**
     * プロジェクトデータをセットする
     * @param {Object} data プロジェクトデータ
     */
    setData(data) {
      this.data.projectName = data.projectName
      this.data.width = data.width
      this.data.height = data.height
      this.data.setLayers(data.layers)
    },

    /**
     * プロジェクトデータをリセットする
     */
    close() {
      this.$reset()
    },

    /**
     * レイヤーを選択する
     * @param {String} layerId レイヤーID
     */
    selectLayer(layerId) {
      this.selectedLayer = layerId
    }
  }
})
