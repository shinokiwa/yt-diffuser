/**
 * components/elements/InputText.vueのテスト
 */
import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import InputSelect from '@/components/elements/InputSelect.vue'

describe('選択フォーム', () => {

    it('id、labelを指定する。idとlabelはFormElementにも送られる。', async () => {
        const com = mount(InputSelect, {
            props: {
                id: 'test',
                label: 'テスト',
            }
        })
        expect(com.find('label').attributes('for')).toBe('test')
        expect(com.find('label').text()).toBe('テスト')

        expect(com.find('select').attributes('id')).toBe('test')
    })


    it('v-modelを使用できる。', async () => {
        let value = 'test'
        const com = mount(InputSelect, {
            props: {
                modelValue: value,
                'onUpdate:modelValue': (v) => value = v
            },
            slots: {
                default: '<option value="test">テスト</option><option value="test2">テスト2</option>'
            }
        })

        expect(com.find('select').element.value).toBe('test')
        com.find('select').setValue('test2')
        await com.vm.$nextTick()
        expect(value).toBe('test2')

    })
})