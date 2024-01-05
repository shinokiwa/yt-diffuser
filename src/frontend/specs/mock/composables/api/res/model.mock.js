/**
 * composables/api/res/model.js のモック
 */
import { vi } from 'vitest'
import { ref } from 'vue'

const mockObj = {
    allModels: ref([]),
    getModels: vi.fn(),
}

export function useModelMock() {
    return mockObj
}
