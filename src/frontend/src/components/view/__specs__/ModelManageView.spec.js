/**
 * components/views/ModelManageView.vue のテスト
 */
import { describe, it, expect } from 'vitest'
import { shallowMount } from '@vue/test-utils'

import ModelManageView from '../ModelManageView.vue'

describe('ModelManageView モデル管理画面', () => {
  it('各子ビューエリアをインポートし、状況によって表示を切り替える。', async () => {
    /**
     * 補足: 左右エリアどちらも機能が多いため、テスト容易性を考慮して、
     * 左右エリアごとにコンポーネントを分割してある。
     */

    // Windowのみスタブ化しない
    const com = shallowMount(ModelManageView, {
      global: {
        stubs: {
          '*': true,
          WindowFrame: false
        }
      }
    })

    // ListAreaは無条件に表示
    expect(com.findComponent({ name: 'ListArea' }).exists()).toBe(true)

    // viewModeがaddの場合、AddArea表示
    com.vm.viewMode = 'add'
    await com.vm.$nextTick()
    expect(com.findComponent({ name: 'AddArea' }).exists()).toBe(true)
    expect(com.findComponent({ name: 'CurrentArea' }).exists()).toBe(false)
    expect(com.findComponent({ name: 'DetailArea' }).exists()).toBe(false)

    // viewModeがcurrentの場合、CurrentArea表示
    com.vm.viewMode = 'current'
    await com.vm.$nextTick()
    expect(com.findComponent({ name: 'AddArea' }).exists()).toBe(false)
    expect(com.findComponent({ name: 'CurrentArea' }).exists()).toBe(true)
    expect(com.findComponent({ name: 'DetailArea' }).exists()).toBe(false)

    // detailModeがmodelの場合、DetailArea表示
    com.vm.viewMode = 'detail'
    await com.vm.$nextTick()
    expect(com.findComponent({ name: 'AddArea' }).exists()).toBe(false)
    expect(com.findComponent({ name: 'CurrentArea' }).exists()).toBe(false)
    expect(com.findComponent({ name: 'DetailArea' }).exists()).toBe(true)
  })
})
