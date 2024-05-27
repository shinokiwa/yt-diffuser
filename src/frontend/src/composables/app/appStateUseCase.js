/**
 * フロントエンド全体の状態を管理するユースケース
 */
import { useAppStateStore } from '@/stores/app/appStateStore'

/**
 * フロントエンド全体の状態を管理するユースケースを返す
 *
 * @returns {ReturnType<typeof AppStateUseCase>}
 */
export function useAppStateUseCase() {
  return AppStateUseCase(useAppStateStore())
}

/**
 * フロントエンド全体の状態を管理するユースケース
 *
 * @param {ReturnType<typeof useAppStateStore>} store
 * @returns {Object}
 */
export function AppStateUseCase(store) {
  return {
    /**
     * リアクティブなフロントエンド状態を取得する
     *
     * @returns {Object} フロントエンド状態
     */
    getRefs: () => store.refs,

    /**
     * ビューを変更する
     *
     * @param {number} view
     */
    changeView(view) {
      store.changeView(view)
    }
  }
}
