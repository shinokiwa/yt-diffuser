import { describe, it, expect, vi } from 'vitest'

vi.mock('@/stores/app/logStore')
import { useLogStore } from '@/stores/app/logStore'

import { useLogUseCase, LogUseCase } from '../logUseCase'

describe('useLogUseCase', () => {
  it('LogUseCase を返す', () => {
    const useCase = useLogUseCase()
    expect(useCase).toHaveProperty('addLog')
    expect(useCase).toHaveProperty('clearLog')
    expect(useCase).toHaveProperty('getToast')
    expect(useLogStore).toHaveBeenCalled()
  })
})

describe('LogUseCase', () => {
  describe('addLog', () => {
    it('ログを追加する。', () => {
      const store = {
        addLog: vi.fn()
      }
      const useCase = LogUseCase(store)

      useCase.addLog('test')
      expect(store.addLog).toHaveBeenCalled()
      expect(store.addLog).toHaveBeenCalledWith('test', false)

      useCase.addLog('test2', true)
      expect(store.addLog).toHaveBeenCalled()
      expect(store.addLog).toHaveBeenCalledWith('test2', true)
    })
  })

  describe('clearLog', () => {
    it('ログをクリアする', () => {
      const store = {
        clearLog: vi.fn()
      }
      const useCase = LogUseCase(store)

      useCase.clearLog()
      expect(store.clearLog).toHaveBeenCalled()
    })
  })

  describe('getToast', () => {
    it('トーストを取得する', () => {
      const store = {
        getToast: vi.fn()
      }
      const useCase = LogUseCase(store)

      useCase.getToast()
      expect(store.getToast).toHaveBeenCalled()
    })
  })
})
