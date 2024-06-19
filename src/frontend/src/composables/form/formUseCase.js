/**
 * フォーム関連のユースケース
 */
import { toRefs } from 'vue'
import { AllFormData } from '@/types/form'
import { useAPI } from '@/adapters/api'
import { useFormStore } from '@/stores/form/formStore'

/**
 * フォームユースケースを返す
 * @returns {ReturnType<typeof FormUseCase>}
 */
export function useFormUseCase() {
  return FormUseCase(useFormStore(), useAPI())
}

/**
 * フォームユースケース
 *
 * @param {ReturnType<typeof useFormStore>} store
 */
export function FormUseCase(store, api) {
  return {
    /**
     * リアクティブなフォームデータを取得する。
     * このユースケースへの入力値はストアにリダイレクトされる。
     *
     * @returns {Object} フォームデータ
     */
    getRefs() {
      // 多いのでまとめて返す
      return toRefs(store.data)
    },

    /**
     * サーバーから最新のフォームデータを取得し、ストアに保存する
     *
     * @returns {Promise<void>}
     */
    async fetch() {
      try {
        const data = await api.get('/api/form')
        const allFormData = new AllFormData(data)
        store.setData(allFormData)
      } catch (e) {
        console.error(e)
        return false
      }
    },

    /**
     * フォームデータをサーバーに送信する
     * @returns {Promise<boolean>}
     */
    async save() {
      try {
        const allFormData = new AllFormData(store.data)
        await api.post('/api/form', allFormData)
        return true
      } catch (e) {
        console.error(e)
        return false
      }
    }
  }
}
