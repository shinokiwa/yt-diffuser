/**
 * baseModel.js のテスト
 */
import { describe, it, expect } from 'vitest'

import { BaseModel } from '../baseModel'

describe('BaseModel', () => {
  it('コンストラクタ', () => {
    const data = {
      model_name: 'model_name',
      screen_name: 'screen_name',
      source: 'source',
      model_class: 'base-model',
      revisions: ['revision'],
      appends: { key: 'value' }
    }
    const baseModel = new BaseModel(data)
    expect(baseModel.model_name).toBe('model_name')
    expect(baseModel.screen_name).toBe('screen_name')
    expect(baseModel.source).toBe('source')
    expect(baseModel.model_class.model_class).toBe('base-model')
    expect(baseModel.revisions.length).toBe(1)
    expect(baseModel.appends.key).toBe('value')
  })
})
