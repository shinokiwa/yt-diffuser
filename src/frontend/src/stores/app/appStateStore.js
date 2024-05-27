/**
 * フロントエンドのアプリケーションの状態を管理するストア
 */
import { defineStore, storeToRefs } from 'pinia'
import { VIEW_IDS } from '@/utils/enum/view'

export const useAppStateStore = defineStore('app-state', {
  state: () => ({
    /**
     * 現在のビュー
     */
    currentView: VIEW_IDS.INITIALIZING
  }),

  getters: {
    /**
     * リアクティブなフロントエンド状態を取得する
     *
     * @returns {Object} フロントエンド状態
     */
    refs() {
      return storeToRefs(this)
    }
  },

  actions: {
    /**
     * ビューを変更する
     *
     * @param {number} view
     */
    changeView(view) {
      this.currentView = view
    }
  }
})
