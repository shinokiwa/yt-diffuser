/**
 * components/views/ModelManageView.vue のテスト
 */
import { describe, it, expect, vi } from 'vitest'
import { shallowMount } from '@vue/test-utils'

import ModelManageView from '@/components/views/ModelManageView.vue'

describe('ModelManageView モデル管理画面', () => {
    it ('各子ビューエリアをインポートし、状況によって表示を切り替える。', async ()=> {
        /**
         * 補足: 左右エリアどちらも機能が多いため、テスト容易性を考慮して、
         * 左右エリアごとにコンポーネントを分割してある。
         */

        // WindowAreaのみスタブ化しない
        const com = shallowMount(ModelManageView, {
            global: {
                stubs: {
                    '*': true,
                    WindowArea: false,
                }
            }
        })

        // ListAreaは無条件に表示
        expect(com.findComponent({name: 'ListArea'}).exists()).toBe(true)

        // detailModeが空の場合、LastuseArea表示
        com.vm.detailMode = ""
        await com.vm.$nextTick()
        expect(com.findComponent({name: 'LastUsedArea'}).exists()).toBe(true)

        // detailModeがaddの場合、AddArea表示
        com.vm.detailMode = "add"
        await com.vm.$nextTick()
        expect(com.findComponent({name: 'AddArea'}).exists()).toBe(true)

        // detailModeがcurrentの場合、CurrentArea表示
        com.vm.detailMode = "current"
        await com.vm.$nextTick()
        expect(com.findComponent({name: 'CurrentArea'}).exists()).toBe(true)

        // detailModeがmodelの場合、DetailArea表示
        com.vm.detailMode = "model"
        await com.vm.$nextTick()
        expect(com.findComponent({name: 'DetailArea'}).exists()).toBe(true)

    })
})