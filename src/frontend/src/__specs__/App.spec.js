// App.vueのテスト
import { describe, it, expect, vi } from 'vitest'
import { shallowMount } from '@vue/test-utils'

vi.mock('@/components/view/HiddenView.vue', () => ({ default: { name: 'HiddenView' } }))
vi.mock('@/components/view/InitializingView.vue', () => ({ default: { name: 'InitializingView' } }))
vi.mock('@/components/view/MenuView.vue', () => ({ default: { name: 'MenuView' } }))
vi.mock('@/components/view/EditorView.vue', () => ({ default: { name: 'EditorView' } }))
vi.mock('@/components/view/ModelManageView.vue', () => ({ default: { name: 'ModelManageView' } }))
vi.mock('@/components/view/ModelView.vue', () => ({ default: { name: 'ModelView' } }))
vi.mock('@/components/view/GalleryView.vue', () => ({ default: { name: 'GalleryView' } }))

vi.mock('@/composables/app/appStateUseCase')
import { Refs } from '@/composables/app/appStateUseCase'

import App from '@/App.vue'
import { VIEW_IDS } from '@/utils/enum/view'

describe('App アプリルート', async () => {
  it('currentViewが変更されると表示するコンポーネントが変わる。', async () => {
    const com = shallowMount(App)
    Refs.currentView.value = VIEW_IDS.MODEL_MANAGE

    await com.vm.$nextTick()

    expect(com.find('.main-view').html()).toContain('model-manage-view-stub')
  })
})
