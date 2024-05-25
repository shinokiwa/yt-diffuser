/**
 * components/elements/InputSeed.vueのテスト
 */
import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import InputSeed from '@/components/elements/InputSeed.vue'

describe('SEED値入力', () => {

    it('id、labelを指定する。idとlabelはFormElementにも送られる。', async () => {
        const com = mount(InputSeed, {
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

    it('typeはtext固定。また、基本的に空欄にならないので、placeholderは対応しない。', async () => {
        const com = mount(InputSeed, {
            props: {
                id: 'test',
                label: 'テスト',
                placeholder: 'テスト',
                type: 'password',
            }
        })
        expect(com.find('input').attributes('placeholder')).toBeUndefined()
        expect(com.find('input').attributes('type')).toBe('text')
    })

    it('v-modelを使用できる。', async () => {
        let value = 'テスト'
        const com = mount(InputSeed, {
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