// view.js のテスト
import { describe, it, expect, vi } from 'vitest'

import { useViewStore } from '@/composables/store/view'

describe('ビューの状態管理', () => {
    
    const { currentView, changeView } = useViewStore()

    it ('初期状態は0', () => {
        expect(currentView.value).toBe(0)
    })

    it ('ビューを変更できる', () => {
        changeView(1)
        expect(currentView.value).toBe(1)
    })
})
