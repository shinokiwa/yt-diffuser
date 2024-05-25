/**
 * composables/api/generate/process.js のモック
 */
import { vi } from 'vitest'
import { ref } from 'vue'

const mockObj = {
    loadModel: vi.fn(),
    removeModel: vi.fn(),
    removeLora: vi.fn(),
}

/**
 * composables/api/generate/status.js のモック
 */
export function useGenerateProcessMock() {
    return mockObj
}