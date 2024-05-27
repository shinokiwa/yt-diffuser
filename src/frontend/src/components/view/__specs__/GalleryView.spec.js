/**
 * GalleryViewのテスト
 */
import { describe, it, expect, vi, afterEach } from 'vitest'
import { shallowMount } from '@vue/test-utils'

import GalleryView from '../GalleryView.vue'

describe('プロジェクト一覧表示ビュー', async () => {
  afterEach(() => {
    vi.resetAllMocks()
  })

  it('プロジェクト一覧が表示される。', async () => {
    const wrapper = shallowMount(GalleryView)
    expect(wrapper.find('#GalleryView').exists()).toBe(true)
  })
})
