/**
 * composables/api/generate/image.js のモック
 */
import { vi } from 'vitest'
import { ref } from 'vue'

const mockObj = {
    start_generate: vi.fn(),
}

/**
 * composables/api/generate/image.js のモック
 */
export function useGenerateImageMock() {
    return mockObj
}