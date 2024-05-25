/**
 * composables/store/toast.jsのモック
 */
import { vi } from 'vitest'
import { ref } from 'vue'

const mockObj = {
    toastQueue: ref([]),
    putToastQueue: vi.fn(),
    getToastQueue: vi.fn(),
}

export function useToastStoreMock() {
    return mockObj
}