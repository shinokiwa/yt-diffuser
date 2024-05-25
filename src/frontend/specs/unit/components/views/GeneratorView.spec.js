/**
 * components/views/GeneratorView.vueのテスト
 */
import { describe, it, expect, vi } from 'vitest'
import { shallowMount } from '@vue/test-utils'

import { useGenerateProgressMock } from '@mocks/composables/api/generate/progress.mock.js'
vi.mock('@/composables/api/generate/progress.js', ()=>({useGenerateProgress: useGenerateProgressMock}))

import { useGenerateImageMock } from '@mocks/composables/api/generate/image.mock.js'
vi.mock('@/composables/api/generate/image.js', ()=>({useGenerateImage: useGenerateImageMock}))

import GeneratorView from '@/components/views/GeneratorView.vue'

describe('連続生成表示', () => {
    const mountOptions = {
        global: {
            stubs: {
                '*': true,
                WindowArea: false,
            }
        }
    }

    it ('生成ボタンを押下すると生成開始', async () => {
        const { start_generate } = useGenerateImageMock()
        const com = shallowMount(GeneratorView, mountOptions)

        const cnt = com.find('#Count')
        cnt.setValue(10)
        const btn = com.find('#StartFromCount')
        btn.trigger('click')
        await com.vm.$nextTick()

        expect(start_generate).toHaveBeenCalled()
        expect(start_generate.mock.calls[0][1]).toBe(10)
    })
})