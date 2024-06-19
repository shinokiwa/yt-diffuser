/**
 * modelUseCase.js のテスト
 */
import { describe, it, expect, vi } from 'vitest'
import { reactive } from 'vue'

vi.mock('@/adapters/api')
import { useAPI } from '@/adapters/api'

vi.mock('@/stores/model/modelStore')
import { useModelStore } from '@/stores/model/modelStore'

import { AllModelData } from '@/types/model'
import { useModelUseCase, ModelUseCase } from '../modelUseCase'

describe('useModelUseCase', () => {
  it('モデル関連のユースケースを生成する', () => {
    const modelUseCase = useModelUseCase()
    expect(modelUseCase).toHaveProperty('getRefs')
    expect(modelUseCase).toHaveProperty('fetchAll')

    expect(useModelStore).toHaveBeenCalled()
    expect(useAPI).toHaveBeenCalled()
  })
})

describe('ModelUseCase', () => {
  describe('getRefs', () => {
    it('リアクティブなモデル一覧を取得する', () => {
      const store = reactive({
        data: {
          baseModels: ['baseModel1'],
          loraModels: ['loraModel1'],
          controlnetModels: ['controlnetModel1']
        }
      })
      const useCase = ModelUseCase(store, {})
      const { baseModels, loraModels, controlnetModels } = useCase.getRefs()

      store.data.baseModels.push('baseModel2')
      store.data.loraModels.push('loraModel2')
      store.data.controlnetModels.push('controlnetModel2')

      expect(baseModels.value).toEqual(['baseModel1', 'baseModel2'])
      expect(loraModels.value).toEqual(['loraModel1', 'loraModel2'])
      expect(controlnetModels.value).toEqual(['controlnetModel1', 'controlnetModel2'])
    })
  })

  describe('fetchAll', () => {
    it('APIから全モデルデータを取得する', async () => {
      const store = {
        setData: vi.fn()
      }
      const api = {
        get: vi.fn().mockResolvedValue({
          baseModels: [
            {
              id: 'test-model-1'
            },
            {
              id: 'test-model-2'
            }
          ]
        })
      }
      const modelUseCase = ModelUseCase(store, api)

      await modelUseCase.fetchAll()

      expect(api.get).toHaveBeenCalledWith('/api/model')
      expect(store.setData).toHaveBeenCalled()
      expect(store.setData.mock.calls[0][0]).toEqual(
        new AllModelData({
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
      )
    })
  })
})
