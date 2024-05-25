// App.vueのテスト
import { describe, it, expect, vi, afterEach } from 'vitest'
import { shallowMount } from '@vue/test-utils'

import { useViewStoreMock } from '@mocks/composables/store/view.mock'
vi.mock('@/composables/store/view', ()=> ({ useViewStore: useViewStoreMock }))

import { useLatestFormMock } from '@mocks/composables/api/res/form/latest.mock'
vi.mock('@/composables/api/res/form/latest', ()=> ({ useLatestForm: useLatestFormMock }))

import { useModelMock } from '@mocks/composables/api/res/model.mock'
vi.mock('@/composables/api/res/model', ()=> ({ useModel: useModelMock }))

afterEach(() => {
    vi.resetAllMocks()
})

import App from '@/App.vue'

describe('App アプリルート', async () => {

    await it ('初期状態ではInitializingViewが表示される。InitializingViewが初期化処理を行い、ビューが変更される想定。', async ()=> {
        const com = shallowMount(App)
        expect(com.find('initializing-view-stub').exists()).toBe(true)
    })

    await it ('現在のビューの内容が変更されると表示するコンポーネントが変わる。', async ()=> {
        const com = shallowMount(App)
        const { currentView, views } = useViewStoreMock()
        currentView.value = views.MODEL_MANAGE

        await com.vm.$nextTick()

        expect(com.find('.main-view').html()).toContain('model-manage-view-stub');
    })
})