/**
 * MenuViewのテスト
 */
import { describe, it, expect, vi, afterEach } from 'vitest'
import { mount } from '@vue/test-utils'

import MenuView from '@/components/views/MenuView.vue'
import { useViewStore } from '@/composables/store/view'

describe('メニューボタン', async () => {

    describe('ナビボタン モデル管理', async () => {

        afterEach(() => {
            vi.resetAllMocks()
        })

        it('currentViewがMODEL_MANAGEの場合のみactiveクラスが付与される。押下するとchangeViewが呼ばれる。', async () => {
            const wrapper = mount(MenuView)
            const changeView = vi.spyOn(wrapper.vm, 'changeView')
            const { currentView, MODEL_MANAGE, GENERATE, GALLERY } = useViewStore()

            currentView.value = -1
            await wrapper.vm.$nextTick()
            let item = wrapper.find('li[role="modelmanage"]')
            expect(item.classes()).not.toContain('active')

            currentView.value = MODEL_MANAGE
            await wrapper.vm.$nextTick()
            expect(item.classes()).toContain('active')

            await item.trigger('click')
            expect(changeView).toHaveBeenCalledWith(MODEL_MANAGE)

            item = wrapper.find('li[role="generate"]')
            await item.trigger('click')
            expect(changeView).toHaveBeenCalledWith(GENERATE)

            item = wrapper.find('li[role="gallery"]')
            await item.trigger('click')
            expect(changeView).toHaveBeenCalledWith(GALLERY)
        })
    })

    describe('通知ボタン', async () => {

        afterEach(() => {
            vi.resetAllMocks()
        })

        it('通知ボタンを押すとtoggleNotificationが呼ばれる。', async () => {
            const wrapper = mount(MenuView)
            const toggleNotificationArea = vi.spyOn(wrapper.vm, 'toggleNotificationArea')

            const item = wrapper.find('li[role="notification"]')
            await item.trigger('click')
            expect(toggleNotificationArea).toHaveBeenCalled()
        })
    })
})
