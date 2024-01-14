/**
 * components/views/ModelManageView.vue のテスト
 */
import { describe, it, expect, vi } from 'vitest'
import { shallowMount } from '@vue/test-utils'

import ModelManageView from '@/components/views/ModelManageView.vue'

describe('ModelManageView モデル管理画面', () => {
    it ('ModelListArea と ModelDetailArea をインポートするだけ。', async ()=> {
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

        expect(com.findComponent({name: 'ModelListArea'}).exists()).toBe(true)
        expect(com.findComponent({name: 'ModelDetailArea'}).exists()).toBe(true)
    })
})