/**
 * appStateUseCase.jsのモック
 */
import { vi } from 'vitest'
import { ref } from 'vue'

export const Refs = {
  currentView: ref(0)
}

export const useAppStateUseCase = vi.fn().mockReturnValue({
  getRefs: vi.fn().mockReturnValue(Refs),
  changeView: vi.fn()
})
