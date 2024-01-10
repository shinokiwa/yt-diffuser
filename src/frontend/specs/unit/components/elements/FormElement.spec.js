// FormElement.vueのテスト
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import FormElement from '@/components/elements/FormElement.vue'

describe('フォーム外枠の表示', () => {
    it('スタイル定義のためだけのコンポーネントなので、特にテストはなし', async () => {
        const com = mount(FormElement)
    })
})