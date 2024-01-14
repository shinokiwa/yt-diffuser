// FormElement.vueのテスト
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import FormElement from '@/components/elements/FormElement.vue'

describe('フォーム外枠の表示', () => {
    it('指定したlabelが表示される。', async () => {
        const com = mount(FormElement, {
            props: {
                label: 'テスト'
            }
        })
        expect(com.find('label').text()).toBe('テスト')
    })

    it('slotに指定した要素が表示される。', async () => {
        const com = mount(FormElement, {
            slots: {
                default: '<div>テスト</div>'
            }
        })
        expect(com.find('div').text()).toBe('テスト')
    })
})
