/**
 * components/views/InitializingView.vueのテスト
 */
import { describe, it, expect, vi, afterEach } from 'vitest'
import { mount } from '@vue/test-utils'

import { useModelMock } from '@mocks/composables/api/res/model.mock'
vi.mock('@/composables/api/res/model', ()=> ({ useModel: useModelMock }))

import { useLatestFormMock } from '@mocks/composables/api/res/form/latest.mock'
vi.mock('@/composables/api/res/form/latest', ()=> ({ useLatestForm: useLatestFormMock }))

import { useViewStoreMock } from '@mocks/composables/store/view.mock'
vi.mock('@/composables/store/view', ()=> ({ useViewStore: useViewStoreMock }))

import { useGenerateStatus } from '@/composables/api/generate/status'
vi.mock('@/composables/api/generate/status', ()=> ({ useGenerateStatus: vi.fn() }))

// fetchとsetTimeoutのモック
const fetchMock = vi.fn()
global.fetch = fetchMock
const setTimeoutMock = vi.fn()
global.setTimeout = setTimeoutMock

import InitializingView from '../InitializingView.vue'

describe('初期化中表示と初期化処理を行う', async () => {

    afterEach(() => {
        vi.resetAllMocks()
    })

    // 初期化処理自体が暫定なので、テストもまだ暫定
    it('マウントするとヘルスチェックを行い、初期化処理を開始する。', async () => {
        fetchMock.mockResolvedValueOnce({ status: 200, ok: true })
        const { changeView, views } = useViewStoreMock()
        const { getModels } = useModelMock()
        const { getLatestForm } = useLatestFormMock()

        const wrapper = mount(InitializingView)

        await wrapper.vm.$nextTick()
        expect(fetchMock).toHaveBeenCalledWith('/api/health')

        await wrapper.vm.$nextTick()
        await wrapper.vm.$nextTick()
        expect(useGenerateStatus).toHaveBeenCalled()

        await wrapper.vm.$nextTick()
        expect(getModels).toHaveBeenCalled()

        await wrapper.vm.$nextTick()
        expect(getLatestForm).toHaveBeenCalled()

        await wrapper.vm.$nextTick()
        expect (changeView).toHaveBeenCalledWith(views.MODEL_MANAGE)
    })
})