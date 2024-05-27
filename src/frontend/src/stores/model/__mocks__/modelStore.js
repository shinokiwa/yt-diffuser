/**
 * modelStore.js のモック
 */
import { vi } from 'vitest'
import { toRefs } from 'vue'

export const ModelStore = {
  data: {
    baseModels: [],
    loraModels: [],
    controlnetModels: []
  },
  get refs() {
    return toRefs(this.data)
  },
  setData: vi.fn()
}

export const useModelStore = vi.fn().mockReturnValue(ModelStore)
