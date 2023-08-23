// InitializingView.vueのテスト
import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'

import InitializingView from '@/components/views/InitializingView.vue'

describe('InitializingView 初期化処理中画面', () => {

    it ('画面表示のみで動作は特にない', async ()=> {
        const com = mount(InitializingView)

        expect(com.find('p').text()).toEqual('初期化中...')
    })
})