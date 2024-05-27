/**
 * apiFormStore.js のテスト
 */
import { describe, it, expect } from 'vitest'
import { isRef } from 'vue'
import { setActivePinia, createPinia } from 'pinia'

import { useFormStore } from '../formStore'

describe('useFormStore フォームストア ', async () => {
  const pinia = createPinia()
  setActivePinia(pinia)

  describe('refs', () => {
    it('リアクティブなフォームデータを取得する', () => {
      const store = useFormStore()
      const refs = store.refs

      expect(isRef(refs.baseModelName)).toBe(true)
      expect(isRef(refs.baseModelRevision)).toBe(true)
      expect(isRef(refs.compile)).toBe(true)
      expect(isRef(refs.loraModelName)).toBe(true)
      expect(isRef(refs.loraModelRevision)).toBe(true)
      expect(isRef(refs.loraModelWeight)).toBe(true)
      expect(isRef(refs.controlnetModelName)).toBe(true)
      expect(isRef(refs.controlnetModelRevision)).toBe(true)
      expect(isRef(refs.controlnetModelWeight)).toBe(true)
      expect(isRef(refs.seed)).toBe(true)
      expect(isRef(refs.generateType)).toBe(true)
      expect(isRef(refs.width)).toBe(true)
      expect(isRef(refs.height)).toBe(true)
      expect(isRef(refs.strength)).toBe(true)
      expect(isRef(refs.prompt)).toBe(true)
      expect(isRef(refs.negativePrompt)).toBe(true)
      expect(isRef(refs.scheduler)).toBe(true)
      expect(isRef(refs.inferenceSteps)).toBe(true)
      expect(isRef(refs.guidanceScale)).toBe(true)
      expect(isRef(refs.memo)).toBe(true)
    })
  })
})
