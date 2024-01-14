/**
 * components/elements/InputText.vueのテスト
 */
import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import InputText from '@/components/elements/InputText.vue'

describe('テキスト入力', () => {

    it('id、labelを指定する。idとlabelはFormElementにも送られる。typeはtext。', async () => {
        const com = mount(InputText, {
            props: {
                id: 'test',
                label: 'テスト',
            }
        })
        expect(com.find('label').attributes('for')).toBe('test')
        expect(com.find('label').text()).toBe('テスト')

        expect(com.find('input').attributes('id')).toBe('test')
        expect(com.find('input').attributes('type')).toBe('text')
    })

    it('placeholderの指定が可能。', async () => {
        const com = mount(InputText, {
            props: {
                id: 'test',
                label: 'テスト',
                placeholder: 'テスト'
            }
        })
        expect(com.find('input').attributes('placeholder')).toBe('テスト')
    })

    it('v-modelを使用できる。', async () => {
        let value = 'テスト'
        const com = mount(InputText, {
            props: {
                modelValue: value,
                'onUpdate:modelValue': (v) => value = v
            },
        })

        expect(com.find('input').element.value).toBe('テスト')
        com.find('input').setValue('テスト2')
        await com.vm.$nextTick()
        expect(value).toBe('テスト2')
    })
})