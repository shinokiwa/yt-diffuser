import { toRef } from 'vue'

import { useAppStateStore } from '@/stores/app/appStateStore'
import { useSessionStorageUseCase } from './sessionStorageUseCase'

/**
 * フロントエンド全体の状態を管理するユースケースを返す
 *
 * @returns {ReturnType<typeof AppStateUseCase>}
 */
export function useAppStateUseCase() {
  return AppStateUseCase(useAppStateStore(), useSessionStorageUseCase())
}

/**
 * フロントエンド全体の状態を管理するユースケース
 *
 * @param {ReturnType<typeof useAppStateStore>} store
 * @returns {Object}
 */
export function AppStateUseCase(store, session) {
  return {
    /**
     * リアクティブなフロントエンド状態を取得する
     *
     * @returns {Object} フロントエンド状態
     */
    getRefs: () => ({
      currentView: toRef(store, 'currentView'),
      isConnected: toRef(store, 'isConnected')
    }),

    /**
     * ビューを変更する
     *
     * @param {number} view
     */
    changeView(view) {
      store.changeView(view)
      session.save()
    }
  }
}
