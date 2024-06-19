/**
 * allModelList.js のテスト
 */
import { describe, it, expect } from 'vitest'

import { AllModelData } from '../allModelData'

describe('AllModel', () => {
  describe('コンストラクタ', () => {
    it('初期値の確認', () => {
      const allModelList = new AllModelData()
      expect(allModelList.baseModels).toEqual([])
      expect(allModelList.loraModels).toEqual([])
      expect(allModelList.controlnetModels).toEqual([])
    })
  })

  describe('setData', () => {
    it('データを入れ替える。', () => {
      const data = {
        baseModels: [
          {
            id: 'model_name1',
            screenName: 'screen_name1',
            source: 'source',
            type: 'base-model',
            revisions: ['revision'],
            appends: { key: 'value' }
          },
          {
            id: 'model_name2',
            screenName: 'screen_name2',
            source: 'source',
            type: 'base-model',
            revisions: ['revision'],
            appends: { key: 'value' }
          }
        ]
      }
      const allModel = new AllModelData()
      allModel.setData(data)
      expect(allModel.baseModels.length).toBe(2)

      const baseModel1 = allModel.baseModels[0]
      expect(baseModel1.id).toBe('model_name1')

      const baseModel2 = allModel.baseModels[1]
      expect(baseModel2.id).toBe('model_name2')
    })
  })
})
