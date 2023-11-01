/**
 * global.jsのテスト
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { ref } from 'vue'

import { useGlobals } from '@/composables/global'

import { useModel } from '@/composables/api/res/model'

vi.mock('@/composables/api/res/model', () => {
    const loadModels = vi.fn()
    const baseModels = ref([])

    const useModel = ()=> {
        return { loadModels, baseModels }
    }

    return { useModel }
})

describe ('init', async () => {
    const { currentView, init } = useGlobals()

    beforeEach(()=>{
        const { loadModels } = useModel()
        loadModels.mockReset()
    })

    it('init実行前のcurrentViewはinitialize', () => {
        expect(currentView.value).toBe('initialize')
    })

    it('initを実行していても、currentViewが変更済みの場合、ユーザー操作があったものと判断して自動設定されない', async () => {
        const { loadModels } = useModel()
        currentView.value = 'test'

        await init()
        expect(loadModels.mock.calls.length).toBe(1)
        expect(currentView.value).toBe('test')
    })

    it('init実行後、ベースモデルが一つも存在しない場合はcurrentViewがmodelmanageになる', async () => {
        const { loadModels } = useModel()
        currentView.value = 'initialize'

        await init()
        expect(loadModels.mock.calls.length).toBe(1)
        expect(currentView.value).toBe('modelmanage')
    })
})
