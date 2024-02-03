/**
 * component/elements/ButtonMenu.jsのテスト
 */
import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'

import ButtonMenu from '@/components/elements/ButtonMenu.vue'

describe('ButtonMenu', () => {
    it('スタイル指定のコンポーネントなので、ロジックはなし。', () => {
        const wrapper = mount(ButtonMenu)
        expect(wrapper.text()).toBe('')
    })
})
