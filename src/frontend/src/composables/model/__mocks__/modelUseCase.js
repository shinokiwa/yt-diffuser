import { vi } from 'vitest'
import { ref } from 'vue'

/**
 * modelUseCase のモック
 */
export const ModelUseCase = (() => {
  const baseModels = ref([])
  const loraModels = ref([])
  const controlnetModels = ref([])

  return {
    getRefs: vi.fn().mockReturnValue({
      baseModels,
      loraModels,
      controlnetModels
    }),
    fetchAll: vi.fn()
  }
})()

/**
 * useModelUseCase のモック
 */
export const useModelUseCase = vi.fn(() => ModelUseCase)
