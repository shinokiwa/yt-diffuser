/**
 * composables/store/notificationArea.jsのモック
 */
import { vi } from 'vitest'
import { ref } from 'vue'

const mockObj = {
    notificationAreaState: ref(false),
    show: vi.fn(),
    hide: vi.fn(),
    toggle: vi.fn(),
}

/**
 * composables/store/notificationArea.jsのモック
 */
export function useNotificationAreaStoreMock() {
    return mockObj
}