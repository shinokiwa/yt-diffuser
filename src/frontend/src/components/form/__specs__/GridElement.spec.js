// GridElement.vueのテスト
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import FormGridElement from '../GridElement.vue'

describe('フォーム項目の外枠', () => {
  it('プロパティとしてidを受け取る。', async () => {
    const com = mount(FormGridElement, {
      props: {
        id: 'test'
      }
    })

    expect(com.props().id).toBe('test')
  })

  it('プロパティとしてlabelを受け取る。', async () => {
    const com = mount(FormGridElement, {
      props: {
        label: 'テスト'
      }
    })
    expect(com.find('label').text()).toBe('テスト')
  })

  it('slotに指定した要素が表示される。', async () => {
    const com = mount(FormGridElement, {
      slots: {
        default: '<div>テスト</div>'
      }
    })
    expect(com.find('div').text()).toBe('テスト')
  })
})
