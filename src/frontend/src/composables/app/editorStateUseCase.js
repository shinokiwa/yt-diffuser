/**
 * エディターの状態を管理するユースケース
 */
import { toRef } from 'vue'

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
     * リアクティブなメインイメージURLを取得する
     *
     * @returns {Ref<string>} メインイメージURL
     */
    getMainImage() {
      return toRef(store, 'mainImage')
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
