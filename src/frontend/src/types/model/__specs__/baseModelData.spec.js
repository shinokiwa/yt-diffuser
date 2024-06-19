/**
 * baseModel.js のテスト
 */
import { describe, it, expect } from 'vitest'

import { ModelType } from '../../enum/model'
import { BaseModelData } from '../baseModelData'

describe('BaseModel', () => {
  it('コンストラクタ', () => {
    const data = {
      id: 'model_name',
      screenName: 'screen_name',
      source: 'source',
      type: ModelType.BASE_MODEL,
      revisions: ['revision'],
      appends: { key: 'value' }
    }
    const baseModel = new BaseModelData(data)
    expect(baseModel.id).toBe('model_name')
    expect(baseModel.screenName).toBe('screen_name')
    expect(baseModel.source).toBe('source')
    expect(baseModel.type).toEqual(ModelType.BASE_MODEL)
    expect(baseModel.revisions.length).toBe(1)
    expect(baseModel.appends.key).toBe('value')
  })
})
