// view.js のテスト
import { describe, it, expect, vi } from 'vitest'

import { useViewStore } from '@/composables/store/view'

describe('ビューの状態管理', () => {
    const { view } = useViewStore()

    it ('初期状態はINITIALIZING', () => {
        expect(view.getCurrent().value).toBe(view.views.INITIALIZING)
    })

    describe('view.change', () => {
        it ('ビューを切り替えられる', () => {
            view.change(view.views.MODEL_MANAGE)
            expect(view.getCurrent().value).toBe(view.views.MODEL_MANAGE)
        })

    })
})

describe('通知エリアの表示状態', () => {
    const { notificationArea } = useViewStore()

    it ('初期状態は非表示', () => {
        expect(notificationArea.getState().value).toBe(false)
    })

    it ('showで通知エリアを表示できる', () => {
        notificationArea.show()
        expect(notificationArea.getState().value).toBe(true)
    })

    it ('hideで通知エリアを非表示にできる', () => {
        notificationArea.hide()
        expect(notificationArea.getState().value).toBe(false)
    })

    it ('toggleで通知エリアの表示状態を切り替えられる', () => {
        notificationArea.toggle()
        expect(notificationArea.getState().value).toBe(true)
        notificationArea.toggle()
        expect(notificationArea.getState().value).toBe(false)
    })
})