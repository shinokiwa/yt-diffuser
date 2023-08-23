/**
 * MenuViewのテスト
 */
import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { ref } from 'vue'

import MenuView from '@/components/views/MenuView.vue'
import { useGlobals } from '@/composables/global.js'

vi.mock('@/composables/global', () => {
    const currentView = ref('')

    const useGlobals = ()=> {
        return { currentView }
    }

    return { useGlobals }
})

describe('メニューボタン', async () => {
    describe('ボタンクリック時の動作', async () => {
        const wrapper = mount(MenuView)

        const {currentView} = useGlobals()

        const views = ['modelmanage', 'generate', 'gallery']
        for (const view of views) {
            currentView.value = ''
            const item = wrapper.find(`li[role="${view}"]`)

            await it ('クリック前はactiveクラスがない', () => {
                expect(item.classes()).not.toContain('active')
            })

            await it ('クリックするとactiveクラスが付与される', async () => {
                await item.trigger('click')

                expect (item.classes()).toContain('active')
            })

            await it ('クリックするとcurrentViewが変更される', () => {
                expect(currentView.value).toBe(view)
            })
        }
    })
})
