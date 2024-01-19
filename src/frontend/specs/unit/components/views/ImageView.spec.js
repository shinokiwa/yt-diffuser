/**
 * components/views/ImageView.vueのテスト
 */
import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'

import { useViewerStoreMock } from '@mocks/composables/store/viewer.mock'
vi.mock('@/composables/store/viewer', ()=>({useViewerStore: useViewerStoreMock}))

import ImageView from '@/components/views/ImageView.vue'

describe('画像表示', () => {
    const mountOptions = {
        global: {
            stubs: {
                teleport: true
            }
        }
    }

    it ('今のところロジックはないので、表示のみ確認', async () => {
        const { isShowViewer } = useViewerStoreMock()
        isShowViewer.value = true
        const com = mount(ImageView, mountOptions)

        expect(com.find('.viewer').exists()).toBe(true)
    })
})