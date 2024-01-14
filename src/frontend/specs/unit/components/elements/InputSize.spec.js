/**
 * components/elements/InputSize.vueのテスト
 */
import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import InputSize from '@/components/elements/InputSize.vue'

describe('サイズ値入力', () => {

    it('id、labelを指定する。idとlabelはFormElementにも送られる。ラベルのforにはWidthの方が指定される。', async () => {
        const com = mount(InputSize, {
            props: {
                id: 'test',
                label: 'テスト',
            }
        })
        expect(com.find('label').attributes('for')).toBe('testWidth')
        expect(com.find('label').text()).toBe('テスト')

        const inputs = com.findAll('input')
        expect(inputs.length).toBe(2)
        expect(inputs.at(0).attributes('id')).toBe('testWidth')
        expect(inputs.at(0).attributes('type')).toBe('text')
        expect(inputs.at(1).attributes('id')).toBe('testHeight')
        expect(inputs.at(1).attributes('type')).toBe('text')
    })

    it('v-modelを使用できる。', async () => {
        let width = 100
        let height = 200
        const com = mount(InputSize, {
            props: {
                width: width,
                'onUpdate:width': (v) => width = v,
                height: height,
                'onUpdate:height': (v) => height = v
            },
        })

        const inputs = com.findAll('input')
        expect(inputs.at(0).element.value).toBe('100')
        expect(inputs.at(1).element.value).toBe('200')

        inputs.at(0).setValue(300)
        inputs.at(1).setValue(400)
        await com.vm.$nextTick()
        expect(width).toBe(300)
        expect(height).toBe(400)
    })
})