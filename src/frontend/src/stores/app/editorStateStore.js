import { defineStore } from 'pinia'
import { ImageFile } from '@/types/image'

export const useEditorStateStore = defineStore('editor-state', {
  state: () => ({
    /**
     * メインエリアの表示状態
     */
    mainArea: 'image'
  }),

  actions: {
    /**
     * メインエリアの表示状態を変更する
     */
    changeMainArea(area) {
      this.mainArea = area
    }
  }
})
