/**
 * 初期化を実行するユースケース
 */
import { useAppStateUseCase, useSessionStorageUseCase } from '@/composables'
import { useFormUseCase } from '@/composables/form/formUseCase'

/**
 * 初期化ユースケースを返す
 *
 * @returns {ReturnType<typeof InitializeUseCase>}
 */
export function useInitializeUseCase() {
  return InitializeUseCase(useAppStateUseCase(), useFormUseCase(), useSessionStorageUseCase())
}

/**
 * 初期化ユースケース
 *
 * @param {ReturnType<typeof useAppStateUseCase>} appState
 * @param {ReturnType<typeof useFormUseCase>} form
 * @returns {Object}
 */
export function InitializeUseCase(appState, form, session) {
  return {
    /**
     * 初期化の実行
     * 各種データの取得と表示フレームの確定
     *
     * @returns {Promise<void>}
     */
    init: async () => {
      // 最後に使用したフォーム情報を取得
      await form.fetch()

      // セッションストレージからデータを取得
      session.load()
    }
  }
}
