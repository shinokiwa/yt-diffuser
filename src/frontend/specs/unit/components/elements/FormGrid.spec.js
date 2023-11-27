// FormGrid.vueのテスト
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import FormGrid from '@/components/elements/FormGrid.vue'

describe('グリッドスタイルのフォーム群', () => {
    it('スタイル定義のためだけのコンポーネントなので、特にテストはなし', async () => {
        const com = mount(FormGrid)
    })
})