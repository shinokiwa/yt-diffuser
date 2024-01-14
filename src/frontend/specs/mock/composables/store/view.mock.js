/**
 * useViewStoreのモック
 */
import { vi } from 'vitest'
import { ref } from 'vue'

const views = {
    INITIALIZING: 0,
    MODEL_MANAGE: 1,
    PROMPT_SETTING: 2,
    GENERATE_BATCH: 3,
    GALLERY: 4,
    EDITOR: 5,
}

const mockObj = {
    currentView: ref(0),
    changeView: vi.fn(),
    views
}

export function useViewStoreMock() {
    return mockObj
}