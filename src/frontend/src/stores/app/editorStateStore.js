/**
 * エディターの状態を管理するストア
 *
 * 仮実装
 */
import { defineStore } from 'pinia'

export const useEditorStateStore = defineStore('editor-state', {
  state: () => ({
    /**
     * 現在のメインイメージ
     */
    mainImage: ''
  }),

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
