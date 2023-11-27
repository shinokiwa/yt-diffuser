// HeaderView.test.js
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import Overlay from '@/components/elements/Overlay.vue'

describe('オーバーレイ', () => {
    const mountOptions = {
        global: {
            stubs: {
                teleport: true
            }
        }
    }

    it('初期状態は非表示', async () => {
        const com = mount(Overlay, mountOptions)
        expect(com.find('.modal-window').exists()).toBe(false)
    })

    it('showメソッドを呼び出すと表示され、hideメソッドで非表示に戻る', async () => {
        const com = mount(Overlay, mountOptions)

        com.vm.show()
        await com.vm.$nextTick()
        expect(com.find('.modal-window').exists()).toBe(true)

        com.vm.hide()
        await com.vm.$nextTick()
        expect(com.find('.modal-window').exists()).toBe(false)
    })
})