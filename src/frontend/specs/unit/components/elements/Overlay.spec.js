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

    it('showメソッドを呼び出すと表示され、hideメソッドで非表示に戻る。それぞれopenイベントとcloseイベントが発火される。', async () => {
        const com = mount(Overlay, mountOptions)

        com.vm.show()
        await com.vm.$nextTick()
        expect(com.find('.modal-window').exists()).toBe(true)
        expect(com.emitted()).toHaveProperty('open')

        com.vm.hide()
        await com.vm.$nextTick()
        expect(com.find('.modal-window').exists()).toBe(false)
        expect(com.emitted()).toHaveProperty('close')
    })

    it('表示切替はv-model:isShowでも可能。', async () => {
        const com = mount(Overlay, {
            ...mountOptions,
            props: {
                isShow: true,
                'onUpdate:isShow': (val) => com.setProps({ isShow: val })
            }
        })

        expect(com.find('.modal-window').exists()).toBe(true)

        com.vm.hide()
        await com.vm.$nextTick()
        expect(com.find('.modal-window').exists()).toBe(false)
        expect(com.props('isShow')).toBe(false)
    })
})