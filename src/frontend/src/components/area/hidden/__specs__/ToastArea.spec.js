import { describe, it, expect, vi, beforeEach } from 'vitest'
import { createTestingPinia } from '@pinia/testing'
import { mount } from '@vue/test-utils'

vi.mock('@/composables/app/logUseCase')
import { useLogUseCase } from '@/composables/app'

import ToastArea from '../ToastArea.vue'

describe('ToastArea トースト通知エリア', () => {
  beforeEach(() => {
    vi.useFakeTimers()
  })

  it('初期状態は非表示。', () => {
    const com = mount(ToastArea)
    expect(com.find('.toast').classes()).not.toContain('show')
    com.unmount()
  })

  it('トースト通知を追加すると表示される。', async () => {
    const com = mount(ToastArea)
    const { getRefs, getToast } = useLogUseCase()
    const { hasToast } = getRefs()
    hasToast.value = true

    getToast.mockReturnValueOnce('テストメッセージ1')

    await com.vm.$nextTick()
    expect(com.find('.toast').classes()).toContain('show')
    expect(com.find('.toast-message').text()).toBe('テストメッセージ1')

    getToast.mockReturnValueOnce('テストメッセージ2')

    vi.advanceTimersToNextTimer()
    await com.vm.$nextTick()
    expect(com.find('.toast').classes()).not.toContain('show')

    vi.advanceTimersToNextTimer()
    await com.vm.$nextTick()
    expect(com.find('.toast').classes()).toContain('show')
    expect(com.find('.toast-message').text()).toBe('テストメッセージ2')
  })
})
