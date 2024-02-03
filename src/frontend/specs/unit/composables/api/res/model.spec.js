/**
 * model.jsのテスト
 */
import { describe, it, expect, vi } from 'vitest'

import { useApiMock } from '@mocks/composables/api/api.mock'
vi.mock('@/composables/api', () => ({ useApi: useApiMock }))

import { useModel } from '@/composables/api/res/model'

describe ('getModels', async () => {
    const { get } = useApiMock()
    const { lastUsedModel, baseModels, loraModels, controlnetModels, getModels } = useModel()

    it ('/api/res/model からモデル一覧を取得し、modelListに格納する。', async () => {
        get.mockReturnValueOnce({
            json: async () => ({
                models: {
                    last_used: {
                        base: { model_name: 'base1' },
                        lora: { model_name: 'lora1' },
                        controlnet: { model_name: 'upscale1' }
                    },
                    hf: [
                        { model_class: 'base-model', model_name: 'base1' },
                        { model_class: 'base-model', model_name: 'base2' },
                        { model_class: 'lora-model', model_name: 'lora1' },
                        { model_class: 'lora-model', model_name: 'lora2' },
                        { model_class: 'controlnet-model', model_name: 'upscale1' },
                        { model_class: 'controlnet-model', model_name: 'upscale2' }
                    ]
                }
            })
        })

        await getModels()
        expect(get).toHaveBeenCalledWith('/api/res/model')

        expect(lastUsedModel.value).toEqual({
            base: { model_name: 'base1' },
            lora: { model_name: 'lora1' },
            controlnet: { model_name: 'upscale1' }
        })
        expect(baseModels.value).toEqual([
            { model_class: 'base-model', model_name: 'base1' },
            { model_class: 'base-model', model_name: 'base2' },
        ])
        expect(loraModels.value).toEqual([
            { model_class: 'lora-model', model_name: 'lora1' },
            { model_class: 'lora-model', model_name: 'lora2' },
        ])
        expect(controlnetModels.value).toEqual([
            { model_class: 'controlnet-model', model_name: 'upscale1' },
            { model_class: 'controlnet-model', model_name: 'upscale2' }
        ])
    })

    it ('レスポンスが空のときはmodelListも空になる', async () => {
        get.mockReturnValueOnce({
            json: async () => ({ models: {} })
        })

        await getModels()
        expect(get).toHaveBeenCalledWith('/api/res/model')
        expect(lastUsedModel.value).toBeUndefined()
        expect(baseModels.value).toEqual([])
        expect(loraModels.value).toEqual([])
        expect(controlnetModels.value).toEqual([])
    })
})
