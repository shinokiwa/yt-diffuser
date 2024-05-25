/**
 * composables/api/res/model.js のモック
 */
import { vi } from 'vitest'
import { ref } from 'vue'

const mockObj = {
    baseModels: ref([]),
    lastUsedModel: ref(null),
    getModels: vi.fn(),
}

export function useModelMock() {
    return mockObj
}
