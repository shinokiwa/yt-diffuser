/**
 * モデル関連の処理を扱うユースケース
 */
import { ref } from 'vue'
import { useModelStore } from '@/stores/model/modelStore'
import { AllModelList } from '@/domains/entity/model/allModelList'
import { useAPI } from '@/adapters/api'

/**
 * モデル関連のユースケースを生成する
 *
 * @param {ReturnType<typeof useAPIModelStore>} store
 * @returns {function(): Promise<ModelList>}
 */
export function useModelUseCase() {
  return ModelUseCase(useModelStore(), useAPI())
}

/**
 * モデル関連のユースケース
 *
 * @param {ReturnType<typeof useModelStore>} store
 */
export function ModelUseCase(store, api) {
  const baseModels = ref([])
  const loraModels = ref([])
  const controlnetModels = ref([])

  return {
    /**
     * リアクティブなモデル一覧を取得する
     */
    getRefs() {
      return {
        baseModels,
        loraModels,
        controlnetModels
      }
    },

    /**
     * APIから全モデルデータを取得する
     * @returns {Promise<AllModelList>}
     */
    async fetchAll() {
      const data = await api.get('/api/res/model')
      const modelList = new AllModelList(data)
      store.setData(modelList.getValues())

      baseModels.value = store.data.baseModels
      loraModels.value = store.data.loraModels
      controlnetModels.value = store.data.controlnetModels

      return modelList
    }
  }
}
