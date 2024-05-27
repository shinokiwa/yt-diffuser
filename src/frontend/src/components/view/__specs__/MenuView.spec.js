/**
 * MenuViewのテスト
 */
import { describe, it, expect, vi, afterEach } from 'vitest'
import { mount } from '@vue/test-utils'

import { useViewStoreMock } from '@mocks/composables/store/view.mock'
vi.mock('@/composables/store/view', () => ({ useViewStore: useViewStoreMock }))

import { useNotificationAreaStoreMock } from '@mocks/composables/store/notificationArea.mock'
vi.mock('@/composables/store/notificationArea', () => ({
  useNotificationAreaStore: useNotificationAreaStoreMock
}))

import MenuView from '../MenuView.vue'

describe('メニューボタン', async () => {
  const wrapper = mount(MenuView)

  describe('ナビボタン モデル管理', async () => {
    afterEach(() => {
      vi.resetAllMocks()
    })

    it('現在のビューに応じたボタンにactiveクラスが付与される。押下するとchangeViewが呼ばれる。', async () => {
      const { currentView, views, changeView } = useViewStoreMock()

      // 通知ボタン以外は全て同じ処理なので、テストを共通化
      const list = [
        { id: 'MenuItemModelManage', view: views.MODEL_MANAGE },
        { id: 'MenuItemGallery', view: views.GALLERY },
        { id: 'MenuItemEditor', view: views.EDITOR }
      ]

      for (const btn of list) {
        currentView.value = views.INITIALIZING
        await wrapper.vm.$nextTick()

        const item = wrapper.find(`li#${btn.id}`)

        expect(item.exists()).toBe(true)
        expect(item.classes()).not.toContain('active')

        await item.trigger('click')
        expect(changeView).toHaveBeenCalledWith(btn.view)
        changeView.mockClear()

        currentView.value = btn.view
        await wrapper.vm.$nextTick()
        expect(item.classes()).toContain('active')
      }
    })
  })
})
