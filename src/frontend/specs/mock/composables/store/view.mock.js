/**
 * useViewStoreのモック
 */
import { vi } from 'vitest'
import { ref } from 'vue'

const currentView = ref(0)
const notificationAreaState = ref(false)

const mockObj = {
    view: {
        getCurrent: ()=> {
            return currentView
        },
        change: vi.fn((number)=>{currentView.value = number}),
        views: {
            INITIALIZING: 0,
            MODEL_MANAGE: 1,
            PROMPT_SETTING: 2,
            GENERATE_BATCH: 3,
            GALLERY: 4,
            EDITOR: 5,
        },
    },
    notificationArea: {
        getState: ()=> {
            return notificationAreaState
        },
        show: vi.fn(),
        hide: vi.fn(),
        toggle: vi.fn(),
    }
}

export function useViewStoreMock() {
    return mockObj
}