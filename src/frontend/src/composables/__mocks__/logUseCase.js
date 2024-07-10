import { vi } from 'vitest'
import { ref } from 'vue'

export const Refs = {
  logs: ref([]),
  toasts: ref([]),
  hasToast: ref(false)
}

export const useLogUseCase = vi.fn().mockReturnValue({
  getRefs: vi.fn().mockReturnValue(Refs),
  addLog: vi.fn(),
  clearLog: vi.fn(),
  getToast: vi.fn()
})
