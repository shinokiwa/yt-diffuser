// InputText.vueのテスト
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { ref } from 'vue'
import InputText from '@/components/elements/InputText.vue'

describe('テキスト入力', () => {

    it('id、label、placeholderプロパティが使える', async () => {
        const com = mount(InputText, {
            props: {
                id: 'test',
                label: 'テスト',
                placeholder: 'テスト入力'
            }
        })

        expect(com.find('label').text()).toBe('テスト')
        expect(com.find('input').attributes('id')).toBe('test')
        expect(com.find('input').attributes('placeholder')).toBe('テスト入力')
    })

    it('v-modelに対応', async () => {
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