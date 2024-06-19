/**
 * apiFormStore.js のテスト
 */
import { describe, it, expect } from 'vitest'
import { toRef } from 'vue'
import { setActivePinia, createPinia } from 'pinia'

import { AllFormData } from '@/types/form'
import { useFormStore } from '../formStore'

describe('useFormStore フォームストア ', async () => {
  const pinia = createPinia()
  setActivePinia(pinia)

  describe('state', () => {
    it('デフォルト値', () => {
      const store = useFormStore()
      store.$reset()

      expect(store.data).instanceOf(AllFormData)
    })
  })

  describe('setData', () => {
    it('データをセットする。', () => {
      const store = useFormStore()
      store.$reset()

      store.setData({
        baseModelID: 'base_model_id',
        baseModelRevision: 'base_model_revision',
        compile: 1,
        loraModelID: 'lora_model_id',
        loraModelRevision: 'lora_model_revision',
        loraModelWeight: 'lora_model_weight',
        controlnetModelID: 'controlnet_model_id',
        controlnetModelRevision: 'controlnet_model_revision',
        controlnetModelWeight: 'controlnet_model_weight',
        seed: 'seed',
        generateType: 'generate_type',
        width: 100,
        height: 200,
        strength: 0.5,
        prompt: 'prompt',
        negativePrompt: 'negative_prompt',
        scheduler: 'scheduler',
        inferenceSteps: 50,
        guidanceScale: 10.0,
        memo: 'memo'
      })

      expect(store.data.baseModelID).toBe('base_model_id')
      expect(store.data.baseModelRevision).toBe('base_model_revision')
      expect(store.data.compile).toBe(1)
    })

    it('データのリアクティブは維持される。', () => {
      const store = useFormStore()
      store.$reset()

      store.setData({
        baseModelID: 'base_model_id',
        baseModelRevision: 'base_model_revision',
        compile: 1,
        loraModelID: 'lora_model_id',
        loraModelRevision: 'lora_model_revision',
        loraModelWeight: 'lora_model_weight',
        controlnetModelID: 'controlnet_model_id',
        controlnetModelRevision: 'controlnet_model_revision',
        controlnetModelWeight: 'controlnet_model_weight',
        seed: 'seed',
        generateType: 'generate_type',
        width: 100,
        height: 200,
        strength: 0.5,
        prompt: 'prompt',
        negativePrompt: 'negative_prompt',
        scheduler: 'scheduler',
        inferenceSteps: 50,
        guidanceScale: 10.0,
        memo: 'memo'
      })

      const baseModelID = toRef(store.data, 'baseModelID')

      store.setData({
        baseModelID: 'base_model_id_2'
      })

      expect(baseModelID.value).toBe('base_model_id_2')
    })
  })
})
