/**
 * フォーム関連のユースケース
 */
import { useAPI } from '@/adapters/api'
import { useFormStore } from '@/stores/form/formStore'
import { FormEntity } from '@/domains/entity/form/form'

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
      return store.refs
    },

    /**
     * フォームデータを取得する
     * こちらはリアクティブではない。
     *
     * @returns {Object} フォームデータ
     */
    getData() {
      return store.data
    },

    /**
     * サーバーから最新のフォームデータを取得し、ストアに保存する
     *
     * @returns {Promise<void>}
     */
    async fetch() {
      try {
        const data = await api.get('/api/form')
        const formEntity = new FormEntity(data)
        store.setData(formEntity.getValues())
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
        const formEntity = new FormEntity(store.data)
        const data = formEntity.getValues()
        await api.post('/api/form', data)
        return true
      } catch (e) {
        console.error(e)
        return false
      }
    }
  }
}
