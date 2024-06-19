/**
 * フォーム値関連のストア
 */
import { defineStore } from 'pinia'
import { AllFormData } from '@/types/form'

/**
 * フォームデータ管理のストアを返す
 *
 */
export const useFormStore = defineStore('form', {
  state: () => ({
    /**
     * フォームデータ
     *
     * @type {AllFormData}
     */
    data: new AllFormData()
  }),

  actions: {
    /**
     * フォームデータをセットする
     *
     * @param {AllFormData | Object} data フォームデータ
     * @returns {void}
     */
    setData(data) {
      this.data.setData(data)
    }
  }
})
