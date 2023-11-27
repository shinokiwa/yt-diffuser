// HeaderView.test.js
import { test, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import HeaderView from '@/components/views/HeaderView.vue'

const mockEventSource = vi.fn()
global.EventSource = mockEventSource

test('テスト項目がないので暫定', () => {
  const com = mount(HeaderView)

  expect(com.find('h1').text()).toBe('ゆとりでふーざー')
})