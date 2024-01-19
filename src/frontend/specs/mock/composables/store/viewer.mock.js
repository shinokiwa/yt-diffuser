/**
 * composables/store/viewer.jsのモック
 */
import { vi } from 'vitest'
import { ref } from 'vue'

const mockObj = {
    isShowViewer: ref(false),
    imageUrl: ref(""),
    nextCallback: ref(null),
    prevCallback: ref(null),
    deleteCallback: ref(null),

    showViewer: vi.fn(),
    hideViewer: vi.fn()
}

export function useViewerStoreMock() {
    return mockObj
}