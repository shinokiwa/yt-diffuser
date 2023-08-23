// InitializingView.vueのテスト
import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'

import ModelManageView from '@/components/views/ModelManageView.vue'

describe('ModelManageView モデル管理画面', () => {

    it ('今のところテスト項目なし', async ()=> {
        const com = mount(ModelManageView)

        expect(com.find('h2').text()).toEqual('モデル一覧')
    })
})