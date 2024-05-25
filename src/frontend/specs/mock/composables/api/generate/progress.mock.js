/**
 * composables/api/generate/progress.js のモック
 */
import { vi } from 'vitest'
import { ref } from 'vue'

const mockObj = {
    generateTotal: ref(0),
    generateCount: ref(0),
    stepsTotal: ref(0),
    stepsCount: ref(0),
    percentage: ref(0),
    elapsed: ref(0),
    remaining: ref(0),
    average: ref(0),
    close: vi.fn(),
}

const generateTotal = ref(0)
const generateCount = ref(0)
const stepsTotal = ref(0)
const stepsCount = ref(0)
const percentage = ref(0)
const elapsed = ref(0)
const remaining = ref(0)
const average = ref(0)

/**
 * composables/api/generate/status.js のモック
 */
export function useGenerateProgressMock() {
    return mockObj
}