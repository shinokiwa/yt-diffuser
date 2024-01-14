/**
 * latest.js のテスト
 */
import { describe, it, expect, vi } from 'vitest'

import { useApiMock } from '@mocks/composables/api/api.mock'
vi.mock('@/composables/api', () => ({ useApi: useApiMock }))

import { useFormStoreMock } from '@mocks/composables/store/form.mock'
vi.mock('@/composables/store/form', () => ({ useFormStore: useFormStoreMock }))

import { useLatestForm } from '@/composables/api/res/form/latest'

describe ('getLatestForm', async () => {
    const { get } = useApiMock()
    const { prompt, negativePrompt } = useFormStoreMock()

    const { getLatestForm } = useLatestForm()

    it ('最新のフォームデータを取得し、store/form.jsに反映する', async () => {

        get.mockReturnValueOnce({
            json: async () => ({
                prompt: 'prompt1',
                negative_prompt: 'negative_prompt1'
            })
        })

        await getLatestForm()
        expect(get).toHaveBeenCalledWith('/api/res/form/latest')

        expect(prompt.value).toEqual('prompt1')
        expect(negativePrompt.value).toEqual('negative_prompt1')
    })
})

describe ('updateLatestForm', async () => {
    const { post } = useApiMock()
    const { prompt, negativePrompt } = useFormStoreMock()

    const { updateLatestForm } = useLatestForm()

    it ('フォームデータを更新する', async () => {
        prompt.value = 'prompt1'
        negativePrompt.value = 'negative_prompt1'

        await updateLatestForm({ prompt, negativePrompt })
        expect(post).toHaveBeenCalledWith('/api/res/form/latest', {
            prompt: 'prompt1',
            negative_prompt: 'negative_prompt1'
        })
    })
})