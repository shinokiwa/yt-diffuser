/**
 * 初期化を実行するユースケース
 */
import { VIEW_IDS } from '@/utils/enum/view'
import { useAppStateUseCase } from '@/composables/app/appStateUseCase'
import { useFormUseCase } from '@/composables/form/formUseCase'

/**
 * 初期化ユースケースを返す
 *
 * @returns {ReturnType<typeof InitializeUseCase>}
 */
export function useInitializeUseCase() {
  return InitializeUseCase(useAppStateUseCase(), useFormUseCase())
}

/**
 * 初期化ユースケース
 *
 * @param {ReturnType<typeof useAppStateUseCase>} appState
 * @param {ReturnType<typeof useFormUseCase>} form
 * @returns {Object}
 */
export function InitializeUseCase(appState, form) {
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

      // 前回使用モデルを取得
      const { baseModelName, baseModelRevision } = form.getData()

      if (baseModelName && baseModelRevision) {
        // 前回使用モデルがある場合はエディター表示
        appState.changeView(VIEW_IDS.EDITOR)
        return
      }

      // 取得できた場合は生成ビュー表示
      // モデル一覧を取得
      // モデルがある場合はモデルセットアップ表示

      // 全て当てはまらない場合はモデル管理表示
      appState.changeView(VIEW_IDS.MODEL_MANAGE)
    }
  }
}
