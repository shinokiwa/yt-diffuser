/**
 * composables/api/generate/status.js のモック
 */
import { vi } from 'vitest'
import { ref } from 'vue'

const mockObj = {
    status: ref(''),
    baseModelLabel: ref(''),
    loraModelLabel: ref(''),
    controlnetModelLabel: ref(''),

    eventSource: null,
    close: vi.fn(),
}

/**
 * composables/api/generate/status.js のモック
 */
export function useGenerateStatusMock() {
    return mockObj
}