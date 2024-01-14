/**
 * composables/store/notificationArea.js のテスト
 */
import { describe, it, expect, vi } from 'vitest'

import { useNotificationAreaStore } from '@/composables/store/notificationArea'

describe('useNotificationAreaStore 通知エリアの表示状態を管理する', () => {
    const { notificationAreaState } = useNotificationAreaStore()

    it ('初期状態は非表示', () => {
        expect(notificationAreaState.value).toBe(false)
    })

    it ('showで通知エリアを表示できる', () => {
        const { show } = useNotificationAreaStore()
        show()
        expect(notificationAreaState.value).toBe(true)
    })

    it ('hideで通知エリアを非表示にできる', () => {
        const { hide } = useNotificationAreaStore()
        hide()
        expect(notificationAreaState.value).toBe(false)
    })

    it ('toggleで通知エリアの表示状態を切り替えられる', () => {
        const { toggle } = useNotificationAreaStore()
        toggle()
        expect(notificationAreaState.value).toBe(true)
        toggle()
        expect(notificationAreaState.value).toBe(false)
    })
})