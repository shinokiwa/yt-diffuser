/**
 * エディターの状態を管理するユースケース
 */

import { useEditorStateStore } from '@/stores/app/editorStateStore'

/**
 * エディターの状態を管理するユースケースを返す
 *
 * @returns {ReturnType<typeof AppStateUseCase>}
 */
export function useEditorStateUseCase() {
  return EditorStateUseCase(useEditorStateStore())
}

/**
 * エディターの状態を管理するユースケース
 *
 * @param {ReturnType<typeof useEditorStateStore>} store
 * @returns {Object}
 */
export function EditorStateUseCase(store) {
  return {
    /**
     * リアクティブなエディター状態を取得する
     *
     * @returns {Object} フロントエンド状態
     */
    getRefs() {
      return store.refs
    },

    /**
     * メインイメージを変更する
     *
     * @param {number} view
     */
    changeMainImage(url) {
      store.changeMainImage(url)
    }
  }
}
