/**
 * ListArea.vue のテスト
 */
import { describe, it, expect } from 'vitest'
import { shallowMount } from '@vue/test-utils'

import ListArea from '../ListArea.vue'

describe('ListArea モデル管理ビュー モデル一覧エリア', () => {
  it('モデル追加ペインとモデル一覧ペインを表示する。', async () => {
    let com = shallowMount(ListArea)

    await com.vm.$nextTick()
    expect(com.find('add-model-pane-stub').exists()).toBe(true)
    expect(com.find('model-list-pane-stub').exists()).toBe(true)
  })
})
