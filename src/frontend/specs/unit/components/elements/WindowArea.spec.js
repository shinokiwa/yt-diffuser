// Window.test.js
import { test, expect, describe, it } from 'vitest'
import { mount } from '@vue/test-utils'
import WindowArea from '@/components/elements/WindowArea.vue'

describe('ウィンドウ表示コンポーネント', () => {

  it('プロパティを何も渡さない場合、単純にslotの内容を表示する。', () => {
    const slots = 'test'
    const com = mount(WindowArea, {
      slots: {
        default: slots
      }
    })

    expect(com.find('div').text()).toBe(slots)
  })

  it('titleプロパティを渡すと、タイトルバーに表示される。', () => {
    const title = 'test'
    const com = mount(WindowArea, {
      props: {
        'window-title': title
      }
    })

    expect(com.find('header').text()).toBe(title)
  })

  it('on-close-buttonプロパティを渡すと、閉じるボタンが表示される。', () => {
    let i = 0
    const com = mount(WindowArea, {
      props: {
        'window-title': 'title',
        'close-button': () => { i++ }
      }
    })

    expect(com.find('button').exists()).toBe(true)
    com.find('button').trigger('click')
    expect(i).toBe(1)
  })
})