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
     * リアクティブな参照を取得する
     *
     * @returns {Object.Ref<string>} メインイメージURL
     */
    getRefs() {
      return {
        mainArea: toRef(store, 'mainArea'),
        mainImage: toRef(store, 'mainImage')
      }
    },

    /**
     * メインエリアをプレビュー画面に変更する
     *
     * @param {number} view
     */
    changeMainToPreview() {
      store.changeMainArea('preview')
    },
    /**
     * メインエリアをレイヤー画面に変更する
     *
     * @param {number} view
     */
    changeMainToLayer() {
      store.changeMainArea('layer')
    },

    /**
     * メインエリアをプロジェクト新規作成画面に変更する
     */
    changeMainToProject() {
      store.changeMainArea('project-new')
    }
  }
}
