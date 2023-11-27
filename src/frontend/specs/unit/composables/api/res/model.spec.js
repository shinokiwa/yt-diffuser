/**
 * model.jsのテスト
 */
import { describe, it, expect, vi } from 'vitest'

import { useModel } from '@/composables/api/res/model'
import { useApi } from '@/composables/api'

vi.mock('@/composables/api', () => {
    const api = {
        get: vi.fn()
    }

    const useApi = ()=> {
        return { api }
    }

    return { useApi }
})

describe ('loadModels', async () => {
    const { api } = useApi()
    const { baseModels, loraModels, upscaleModels, loadModels } = useModel()

    it ('モデルをロードすると各Modelsに値が入る', async () => {
        api.get.mockReturnValueOnce({
            data: {
                base: ['base1', 'base2'],
                lora: ['lora1', 'lora2'],
                upscale: ['upscale1', 'upscale2']
            }
        })

        await loadModels()
        expect(api.get).toHaveBeenCalledWith('/api/res/model')
        expect(baseModels.value).toEqual(['base1', 'base2'])
        expect(loraModels.value).toEqual(['lora1', 'lora2'])
        expect(upscaleModels.value).toEqual(['upscale1', 'upscale2'])
    })

    it ('レスポンスが空のときは各Modelsも空になる', async () => {
        api.get.mockReturnValueOnce({
            data: {}
        })

        await loadModels()
        expect(api.get).toHaveBeenCalledWith('/api/res/model')
        expect(baseModels.value).toEqual([])
        expect(loraModels.value).toEqual([])
        expect(upscaleModels.value).toEqual([])
    })
})
