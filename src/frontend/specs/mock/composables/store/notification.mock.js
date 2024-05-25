/**
 * composables/store/notification.jsのモック
 */
import { vi } from 'vitest'
import { ref } from 'vue'

const mockObj = {
    notificationList: ref([]),
    addNotification: vi.fn(),
    removeNotification: vi.fn(),
    clearNotification: vi.fn(),
}

export function useNotificationStoreMock() {
    return mockObj
}