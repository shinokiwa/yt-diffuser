/**
 * composables/api/index.js のモック
 */
import { vi } from 'vitest'

const mockObj = {
    get: vi.fn(),
    post: vi.fn(),
    del: vi.fn(),
}

export function useApiMock() {
    return mockObj
}
