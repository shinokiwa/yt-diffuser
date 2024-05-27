/**
 * allModelList.js のテスト
 */
import { describe, it, expect } from 'vitest'

import { AllModelList } from '@/domains/entity/model/allModelList'

describe('AllModelList', () => {
  it('コンストラクタ', () => {
    const data = {
      models: [
        {
          model_name: 'model_name1',
          screen_name: 'screen_name1',
          source: 'source',
          model_class: 'base-model',
          revisions: ['revision'],
          appends: { key: 'value' }
        },
        {
          model_name: 'model_name2',
          screen_name: 'screen_name2',
          source: 'source',
          model_class: 'base-model',
          revisions: ['revision'],
          appends: { key: 'value' }
        }
      ]
    }
    const allModelList = new AllModelList(data)
    expect(allModelList.baseModels.length).toBe(2)

    const baseModel1 = allModelList.baseModels[0]
    expect(baseModel1.model_name).toBe('model_name1')

    const baseModel2 = allModelList.baseModels[1]
    expect(baseModel2.model_name).toBe('model_name2')
  })
})
