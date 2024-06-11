/**
 * フォーム値関連のストア
 */
import { defineStore } from 'pinia'
import { toRefs } from 'vue'

/**
 * フォームデータ管理のストアを返す
 *
 */
export const useFormStore = defineStore('form', {
  state: () => ({
    /**
     * フォームデータ
     */
    data: {
      baseModelID: '',
      baseModelRevision: '',
      compile: 0,

      loraModelID: '',
      loraModelRevision: '',
      loraModelWeight: '',

      controlnetModelID: '',
      controlnetModelRevision: '',
      controlnetModelWeight: '',

      seed: 0,
      generateType: 't2i',

      width: 1024,
      height: 1024,

      strength: 0.3,

      prompt: '',
      negativePrompt: '',
      scheduler: 'ddim',
      inferenceSteps: 30,
      guidanceScale: 8.0,

      memo: ''
    }
  }),

  getters: {
    /**
     * リアクティブなフォームデータを取得する
     *
     * @returns {Object} フォームデータ
     */
    refs(state) {
      return toRefs(state.data)
    }
  },

  actions: {
    /**
     * フォームデータをセットする
     *
     * @param {Object} data フォームデータ
     * @returns {void}
     */
    setData(data) {
      for (const key in this.data) {
        this.data[key] = data[key]
      }
    }
  }
})
