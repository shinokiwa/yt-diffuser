/**
 * modelUseCase.js のテスト
 */
import { describe, it, expect, vi } from 'vitest'
import { isRef } from 'vue'

vi.mock('@/adapters/api')
import { useAPI, API } from '@/adapters/api'

vi.mock('@/stores/model/modelStore')
import { useModelStore, ModelStore } from '@/stores/model/modelStore'

import { useModelUseCase } from '../modelUseCase'

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
      const modelUseCase = useModelUseCase()
      const { baseModels, loraModels, controlnetModels } = modelUseCase.getRefs()

      expect(isRef(baseModels)).toBe(true)
      expect(isRef(loraModels)).toBe(true)
      expect(isRef(controlnetModels)).toBe(true)

      ModelStore.data.baseModels = ['baseModel']
      ModelStore.data.loraModels = ['loraModel']
      ModelStore.data.controlnetModels = ['controlnetModel']

      expect(baseModels.value).toEqual(['baseModel'])
      expect(loraModels.value).toEqual(['loraModel'])
      expect(controlnetModels.value).toEqual(['controlnetModel'])
    })
  })

  describe('fetchAll', () => {
    it('APIから全モデルデータを取得する', async () => {
      const modelUseCase = useModelUseCase()
      const modelList = {
        models: [
          { modelName: 'model1', modelClass: 'base-model' },
          { modelName: 'model2', modelClass: 'base-model' }
        ]
      }
      API.get.mockResolvedValue(modelList)

      await modelUseCase.fetchAll()

      expect(API.get).toHaveBeenCalledWith('/api/res/model')
      expect(ModelStore.setData).toHaveBeenCalled()
    })

    it.todo('APIのほうも修正したいので、ちょっとまだテストが雑')
  })
})
