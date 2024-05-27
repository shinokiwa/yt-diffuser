/**
 * EditorViewのテスト
 */
import { describe, it, expect, vi, afterEach } from 'vitest'
import { shallowMount } from '@vue/test-utils'

import EditorView from '../EditorView.vue'

describe('エディタービュー', async () => {

    afterEach(() => {
        vi.resetAllMocks()
    })

    it('エディターが表示される。', async () => {
        const wrapper = shallowMount(EditorView)

        expect(wrapper.find('div#EditorView').exists()).toBe(true)
        expect(wrapper.find('main-area-stub').exists()).toBe(true)
        expect(wrapper.find('prompt-area-stub').exists()).toBe(true)
        expect(wrapper.find('layer-area-stub').exists()).toBe(true)
        expect(wrapper.find('result-area-stub').exists()).toBe(true)
    })
})