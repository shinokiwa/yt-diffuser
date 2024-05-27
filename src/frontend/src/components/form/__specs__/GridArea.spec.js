// FormGrid.vueのテスト
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import FormGridArea from '../GridArea.vue'

describe('フォームのグリッドレイアウト', () => {
  it('プロパティとしてidを受け取る。', async () => {
    const com = mount(FormGridArea, {
      props: {
        id: 'test'
      }
    })

    expect(com.props().id).toBe('test')
  })
})
