import { describe, it, expect } from 'vitest'

import { AllFormData } from '../allFormData'

describe('AllFormData', () => {
  describe('コンストラクタ', () => {
    it('デフォルト値', () => {
      const allFormData = new AllFormData()
      expect(allFormData.baseModelID).toBe('')
      expect(allFormData.baseModelRevision).toBe('')
      expect(allFormData.compile).toBe(0)
      expect(allFormData.loraModelID).toBe('')
      expect(allFormData.loraModelRevision).toBe('')
      expect(allFormData.loraModelWeight).toBe('')
      expect(allFormData.controlnetModelID).toBe('')
      expect(allFormData.controlnetModelRevision).toBe('')
      expect(allFormData.controlnetModelWeight).toBe('')
      expect(allFormData.seed).toBeNull()
      expect(allFormData.generateType).toBe('t2i')
      expect(allFormData.width).toBe(1024)
      expect(allFormData.height).toBe(1024)
      expect(allFormData.strength).toBe(0.3)
      expect(allFormData.prompt).toBe('')
      expect(allFormData.negativePrompt).toBe('')
      expect(allFormData.scheduler).toBe('ddim')
      expect(allFormData.inferenceSteps).toBe(30)
      expect(allFormData.guidanceScale).toBe(8.0)
      expect(allFormData.memo).toBe('')
    })
  })
  describe('setData', () => {
    it('値をセットする', () => {
      const allFormData = new AllFormData()
      allFormData.setData({
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

      expect(allFormData.baseModelID).toBe('base_model_id')
      expect(allFormData.baseModelRevision).toBe('base_model_revision')
      expect(allFormData.compile).toBe(1)
      expect(allFormData.loraModelID).toBe('lora_model_id')
      expect(allFormData.loraModelRevision).toBe('lora_model_revision')
      expect(allFormData.loraModelWeight).toBe('lora_model_weight')
      expect(allFormData.controlnetModelID).toBe('controlnet_model_id')
      expect(allFormData.controlnetModelRevision).toBe('controlnet_model_revision')
      expect(allFormData.controlnetModelWeight).toBe('controlnet_model_weight')
      expect(allFormData.seed).toBe('seed')
      expect(allFormData.generateType).toBe('generate_type')
      expect(allFormData.width).toBe(100)
      expect(allFormData.height).toBe(200)
      expect(allFormData.strength).toBe(0.5)
      expect(allFormData.prompt).toBe('prompt')
      expect(allFormData.negativePrompt).toBe('negative_prompt')
      expect(allFormData.scheduler).toBe('scheduler')
      expect(allFormData.inferenceSteps).toBe(50)
      expect(allFormData.guidanceScale).toBe(10.0)
      expect(allFormData.memo).toBe('memo')
    })
  })
})
