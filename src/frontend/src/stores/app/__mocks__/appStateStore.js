/**
 * appStateStore.js のモック
 *
 */
import { vi } from 'vitest'

export const AppStateStore = (() => {
  const _refs = vi.fn()

  return {
    _refs,
    get refs() {
      return _refs()
    },
    changeView: vi.fn()
  }
})()

export const useAppStateStore = vi.fn().mockReturnValue(AppStateStore)
