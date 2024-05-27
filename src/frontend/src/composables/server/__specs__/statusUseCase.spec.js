/**
 * statusUseCase.js のテスト
 */
import { describe, it, expect, vi } from 'vitest'

vi.mock('@/adapters/api')
import { useAPI } from '@/adapters/api'

vi.mock('@/stores/server/statusStore')
import { useServerStatusStore, ServerStatusStore } from '@/stores/server/statusStore'

import { useServerStatusUseCase, ServerStatusUseCase } from '../statusUseCase'

describe('useServerStatusUseCase', () => {
  it('ServerStatusUseCase を返す', () => {
    const useCase = useServerStatusUseCase()
    expect(useCase).toBeInstanceOf(Object)

    expect(useAPI).toHaveBeenCalled()
    expect(useServerStatusStore).toHaveBeenCalled()
  })
})

describe('HealthCheckUseCase', () => {
  describe.skip('open', () => {
    it('ややこしいので現状スキップ。', async () => {})
  })
})
