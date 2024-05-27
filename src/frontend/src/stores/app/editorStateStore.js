/**
 * エディターの状態を管理するストア
 *
 * 仮実装
 */
import { defineStore, storeToRefs } from 'pinia'

export const useEditorStateStore = defineStore('Editor-state', {
  state: () => ({
    /**
     * 現在のメインイメージ
     */
    mainImage: ''
  }),

  getters: {
    refs() {
      return storeToRefs(this)
    }
  },

  actions: {
    /**
     * メインイメージを変更する
     *
     * @param {string} url
     */
    changeMainImage(url) {
      this.mainImage = url
    }
  }
})
