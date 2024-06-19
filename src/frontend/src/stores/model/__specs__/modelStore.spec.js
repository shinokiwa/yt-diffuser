/**
 * modelStore.js のテスト
 */
import { describe, it, expect } from 'vitest'
import { toRef } from 'vue'
import { setActivePinia, createPinia } from 'pinia'

import { AllModelData } from '@/types/model'

import { useModelStore } from '../modelStore'

describe('useModelStore モデル管理のストア', () => {
  const pinia = createPinia()
  setActivePinia(pinia)

  describe('setData', () => {
    it('モデルデータをセットする', () => {
      const store = useModelStore()
      store.$reset()
      const data = new AllModelData({
        baseModels: [
          {
            id: 'test-model-1'
          },
          {
            id: 'test-model-2'
          }
        ],
        loraModels: [],
        controlnetModels: []
      })
      store.setData(data)

      expect(store.data.baseModels).toEqual(data.baseModels)
      expect(store.data.loraModels).toEqual(data.loraModels)
      expect(store.data.controlnetModels).toEqual(data.controlnetModels)
    })

    it('データのリアクティブは維持される。', () => {
      const store = useModelStore()
      store.$reset()
      const data = new AllModelData({
        baseModels: [
          {
            id: 'test-model-1'
          },
          {
            id: 'test-model-2'
          }
        ],
        loraModels: [],
        controlnetModels: []
      })
      store.setData(data)

      const baseModels = toRef(store.data, 'baseModels')

      const data2 = {
        baseModels: [
          {
            id: 'test-model-3'
          }
        ],
        loraModels: [],
        controlnetModels: []
      }

      store.setData(data2)
      expect(baseModels.value[0].id).toEqual('test-model-3')
    })
  })
})
