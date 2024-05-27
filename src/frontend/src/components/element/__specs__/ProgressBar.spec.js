// HeaderView.test.js
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import ProgressBar from '../ProgressBar.vue'

describe('プログレスバー', () => {

    const com = mount(ProgressBar, {
        propsData: {
            value: 0
        }
    })

    it('渡されたvalueに応じてバーの長さが変わる', async () => {
        await com.setProps({ value: 50 })
        expect(com.find('.progress-bar .bar').element.style.width).toBe('50%');

        await com.setProps({ value: 0 })
        expect(com.find('.progress-bar .bar').element.style.width).toBe('0%');

        await com.setProps({ value: 100 })
        expect(com.find('.progress-bar .bar').element.style.width).toBe('100%');
    })
})