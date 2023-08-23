// InitializingView.vueのテスト
import { describe, it, expect, vi } from 'vitest'
import { shallowMount } from '@vue/test-utils'
import { nextTick, ref } from 'vue'

import { useGlobals } from '@/composables/global.js'

import App from '@/App.vue'

vi.mock('@/composables/global', () => {
    const init = vi.fn()
    const currentView = ref ('initialize')

    return {
        useGlobals: () => {
            return { 
                currentView,
                init
            }
        }
    }
})

describe('App アプリルート', () => {
    const com = shallowMount(App)

    it ('読み込むと初期化処理を開始する', async ()=> {
        const { init } = useGlobals()
        await nextTick()

        // initが一回実行されれば良い
        expect(init.mock.calls.length).toBe(1)
    })

    it ('currentViewの内容が変更されると表示するコンポーネントが変わる', async ()=> {
        const { currentView } = useGlobals()

        await nextTick()
        expect(com.find('#ContentWrapper > *').html()).toContain('initializing-view-stub');

        currentView.value = 'modelmanage'
        await nextTick()
        expect(com.find('#ContentWrapper > *').html()).toContain('model-manage-view-stub');
    })
})