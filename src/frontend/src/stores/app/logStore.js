import { defineStore } from 'pinia'

export const useLogStore = defineStore('log', {
  state: () => ({
    /**
     * ログ
     */
    logs: [],
    toasts: []
  }),

  getters: {
    /**
     * トーストがあるかどうか
     */
    hasToast() {
      return this.toasts.length > 0
    }
  },

  actions: {
    /**
     * ログを追加する
     *
     * @param {string} log
     */
    addLog(log, isToast = false) {
      this.logs.push(log)
      if (isToast) {
        this.toasts.push(log)
      }
    },

    /**
     * ログをクリアする
     */
    clearLog() {
      this.logs = []
    },

    /**
     * トーストを取得する。
     * トーストは取得後にクリアされる。
     */
    getToast() {
      const toast = this.toasts.shift()
      return toast
    }
  }
})
