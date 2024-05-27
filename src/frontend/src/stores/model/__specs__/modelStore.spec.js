/**
 * modelStore.js のテスト
 */
import { describe, it, expect } from 'vitest'
import { isRef } from 'vue'
import { setActivePinia, createPinia } from 'pinia'

import { useModelStore } from '../modelStore'

describe('useModelStore モデル管理のストア', () => {
  const pinia = createPinia()
  setActivePinia(pinia)

  describe('refs', () => {
    it('モデルデータを取得する', () => {
      const store = useModelStore()
      const refs = store.refs
      expect(isRef(refs.baseModels)).toBe(true)
      expect(isRef(refs.loraModels)).toBe(true)
      expect(isRef(refs.controlnetModels)).toBe(true)
    })
  })

  describe('setData', () => {
    it('モデルデータをセットする', () => {
      const store = useModelStore()
      const data = {
        baseModels: ['base'],
        loraModels: ['lora'],
        controlnetModels: ['controlnet']
      }
      store.setData(data)
      expect(store.data.baseModels).toEqual(data.baseModels)
      expect(store.data.loraModels).toEqual(data.loraModels)
      expect(store.data.controlnetModels).toEqual(data.controlnetModels)
    })
  })
})
