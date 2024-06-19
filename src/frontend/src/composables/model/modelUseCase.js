/**
 * モデル関連の処理を扱うユースケース
 */
import { toRef } from 'vue'
import { useAPI } from '@/adapters/api'
import { useModelStore } from '@/stores/model/modelStore'
import { AllModelData } from '@/types/model'

/**
 * モデル関連のユースケースを生成する
 *
 * @param {ReturnType<typeof useAPIModelStore>} store
 * @param {ReturnType<typeof useAPI>} api
 * @returns {ReturnType<typeof ModelUseCase>}
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
  return {
    /**
     * リアクティブなモデル一覧を取得する
     */
    getRefs() {
      return {
        baseModels: toRef(store.data, 'baseModels'),
        loraModels: toRef(store.data, 'loraModels'),
        controlnetModels: toRef(store.data, 'controlnetModels')
      }
    },

    /**
     * APIから全モデルデータを取得する
     * @returns {Promise <AllModelData>}
     */
    async fetchAll() {
      const data = await api.get('/api/model')
      const allModels = new AllModelData(data)
      store.setData(allModels)
      return allModels
    },

    /**
     * モデル名からモデルデータを取得する
     *
     */
    findModelByID(id) {
      const model = store.findModelByID(id)
      return model
    },

    /**
     * モデルをロードする
     */
    async loadModel(base_model_id, base_revision, compile) {
      await api.post('/api/model/load', {
        base_model_id,
        base_revision,
        compile
      })
    },

    /**
     * モデルを解放する
     */
    async releaseModel() {
      await api.get('/api/model/exit')
    }
  }
}
