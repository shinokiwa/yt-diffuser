/**
 * フロントエンドのアプリケーションの状態を管理するストア
 */
import { defineStore } from 'pinia'
import { VIEW_IDS } from '@/types/enum/view'

export const useAppStateStore = defineStore('app-state', {
  state: () => ({
    /**
     * 現在のビュー
     */
    currentView: VIEW_IDS.INITIALIZING,
    isConnected: false
  }),

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
