// App.vueのテスト
import { describe, it, expect, vi, afterEach } from 'vitest'
import { shallowMount } from '@vue/test-utils'
import { ref } from 'vue'

import App from '@/App.vue'

const readyState = ref(false)
const ready = vi.fn()
vi.mock('@/composables/store/app', ()=> {
    return { useAppStore: ()=> { return { readyState, ready } } }
})

const currentView = ref(0)
const changeView = vi.fn()
const MODEL_MANAGE = 1
vi.mock('@/composables/store/view', ()=> {
    return { useViewStore: ()=> { return { currentView, changeView, MODEL_MANAGE } } }
})

const loadModels = vi.fn()
const baseModels = ref([])
vi.mock('@/composables/api/res/model', ()=> {
    return { useModel: ()=> { return {loadModels, baseModels} } }
})

afterEach(() => {
    vi.resetAllMocks()
})


describe('App アプリルート', async () => {

    await it ('読み込むと初期化処理を実行し、完了したらready()により初期化完了となる。', async ()=> {
        const com = shallowMount(App)
        await com.vm.$nextTick()
        expect(ready).toHaveBeenCalledTimes(1)
        com.unmount()
    })

    await it ('初期状態ではInitializingViewが表示される。初期化完了するとビューが表示される。', async ()=> {
        const com = shallowMount(App)
        await com.vm.$nextTick()
        expect(com.find('#InitializingView').isVisible()).toBe(true)

        readyState.value = true
        await com.vm.$nextTick()
        expect(com.find('#InitializingView').exists()).toBe(false)
        com.unmount()
    })

    await it ('currentViewの内容が変更されると表示するコンポーネントが変わる。', async ()=> {
        const com = shallowMount(App)
        readyState.value = true
        currentView.value = MODEL_MANAGE
        await com.vm.$nextTick()

        expect(com.find('.main-view').html()).toContain('model-manage-view-stub');
        com.unmount()
    })
})