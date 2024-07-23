/**
 * 初期化を実行するユースケース
 */
import { useAppStateUseCase, useSessionStorageUseCase, useProjectUseCase } from '@/composables'
import { useFormUseCase } from '@/composables/form/formUseCase'

/**
 * 初期化ユースケースを返す
 *
 * @returns {ReturnType<typeof InitializeUseCase>}
 */
export function useInitializeUseCase() {
  return InitializeUseCase(
    useAppStateUseCase(),
    useFormUseCase(),
    useSessionStorageUseCase(),
    useProjectUseCase()
  )
}

/**
 * 初期化ユースケース
 *
 * @param {ReturnType<typeof useAppStateUseCase>} appState
 * @param {ReturnType<typeof useFormUseCase>} form
 * @param {ReturnType<typeof useSessionStorageUseCase>} session
 * @param {ReturnType<typeof useProjectUseCase>} project
 * @returns {Object}
 */
export function InitializeUseCase(appState, form, session, project) {
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

      await project.loadDeffered()
    }
  }
}
