import { toRef } from 'vue'

import { useLogStore } from '@/stores/app/logStore'

/**
 * ログを管理するユースケースを返す
 *
 * @returns {ReturnType<typeof LogUseCase>}
 */
export function useLogUseCase() {
  return LogUseCase(useLogStore())
}

/**
 * ログを管理するユースケース
 *
 * @param {ReturnType<typeof useLogStore>} store
 * @returns {Object}
 */
export function LogUseCase(store) {
  return {
    /**
     * ストアへの参照を返す
     */
    getRefs() {
      return {
        logs: toRef(store, 'logs'),
        toasts: toRef(store, 'toasts'),
        hasToast: toRef(store, 'hasToast')
      }
    },

    /**
     * ログを追加する
     *
     * @param {string} log
     */
    addLog(log, isToast = false) {
      store.addLog(log, isToast)
    },

    /**
     * ログをクリアする
     */
    clearLog() {
      store.clearLog()
    },

    /**
     * トーストを取得する。
     * トーストは取得後にクリアされる。
     */
    getToast() {
      return store.getToast()
    }
  }
}
