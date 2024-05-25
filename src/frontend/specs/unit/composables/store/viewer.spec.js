/**
 * composables/store/viewer.jsのテスト
 */
import { describe, it, expect, vi } from 'vitest'

import { useViewerStore } from '@/composables/store/viewer'

describe('画像ビューワーの状態管理', () => {

    describe('showViewer', () => {
        it ('画像ビューワーを表示できる', () => {
            const { showViewer, isShowViewer, imageUrl, nextCallback, prevCallback, deleteCallback } = useViewerStore()
            showViewer("test", "next", "prev", "delete")

            expect(isShowViewer.value).toBe(true)
            expect(imageUrl.value).toBe("test")
            expect(nextCallback.value).toBe("next")
            expect(prevCallback.value).toBe("prev")
            expect(deleteCallback.value).toBe("delete")
        })
    })

    describe('hideViewer', () => {
        it ('画像ビューワーを非表示にできる', () => {
            const { hideViewer, isShowViewer } = useViewerStore()
            isShowViewer.value = true
            hideViewer()

            expect(isShowViewer.value).toBe(false)
        })
    })
})