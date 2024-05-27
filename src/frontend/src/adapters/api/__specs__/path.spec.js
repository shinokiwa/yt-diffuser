/**
 * path.js のテスト
 */
import { describe, it, expect } from 'vitest'
import { createPath } from '../path'

describe('createPath', () => {
  it('パラメータがない場合はクエリストリングを付与しない。', () => {
    const apiPath = createPath('/api/res/model')
    expect(apiPath).toBe('/api/res/model')
  })

  it('パラメータが空の場合はクエリストリングを付与しない。', () => {
    const apiPath = createPath('/api/res/model', {})
    expect(apiPath).toBe('/api/res/model')
  })

  it('パラメータが複数ある場合はクエリストリングを付与する。', () => {
    const apiPath = createPath('/api/res/model', { key1: 'value1', key2: 'value2' })
    expect(apiPath).toBe('/api/res/model?key1=value1&key2=value2')
  })
})
