/**
 * composables/api/res/form/latest.js のモック
 */
import { vi } from 'vitest'

const mockObj = {
    getLatestForm: vi.fn(),
    updateLatestForm: vi.fn(),
}

export function useLatestFormMock() {
    return mockObj
}