/**
 * model.jsのテスト
 */
import { describe, it, expect, vi } from 'vitest'

import { useApiMock } from '@mocks/composables/api/api.mock'
vi.mock('@/composables/api', () => ({ useApi: useApiMock }))

import { useModel } from '@/composables/api/res/model'

describe ('getModels', async () => {
    const { get } = useApiMock()
    const { modelList, getModels } = useModel()

    it ('/api/res/model からモデル一覧を取得し、modelListに格納する。', async () => {
        get.mockReturnValueOnce({
            json: async () => ({
                models: [
                    { model_class: 'base-model', model_name: 'base1' },
                    { model_class: 'base-model', model_name: 'base2' },
                    { model_class: 'lora-model', model_name: 'lora1' },
                    { model_class: 'lora-model', model_name: 'lora2' },
                    { model_class: 'controlnet-model', model_name: 'upscale1' },
                    { model_class: 'controlnet-model', model_name: 'upscale2' }
                ]
            })
        })

        await getModels()
        expect(get).toHaveBeenCalledWith('/api/res/model')

        expect(modelList.value).toEqual([
            { model_class: 'base-model', model_name: 'base1' },
            { model_class: 'base-model', model_name: 'base2' },
            { model_class: 'lora-model', model_name: 'lora1' },
            { model_class: 'lora-model', model_name: 'lora2' },
            { model_class: 'controlnet-model', model_name: 'upscale1' },
            { model_class: 'controlnet-model', model_name: 'upscale2' }
        ])
    })

    it ('レスポンスが空のときはmodelListも空になる', async () => {
        get.mockReturnValueOnce({
            json: async () => ({ models: [] })
        })

        await getModels()
        expect(get).toHaveBeenCalledWith('/api/res/model')
        expect(modelList.value).toEqual([])
    })
})
