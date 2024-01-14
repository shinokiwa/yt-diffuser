// view.js のテスト
import { describe, it, expect, vi } from 'vitest'

import { useViewStore } from '@/composables/store/view'

describe('ビューの状態管理', () => {
    const { views, currentView } = useViewStore()

    it ('初期状態はINITIALIZING', () => {
        expect(currentView.value).toBe(views.INITIALIZING)
    })

    describe('change', () => {
        it ('ビューを切り替えられる', () => {
            const { changeView } = useViewStore()
            changeView(views.MODEL_MANAGE)

            expect(currentView.value).toBe(views.MODEL_MANAGE)
        })
    })
})
