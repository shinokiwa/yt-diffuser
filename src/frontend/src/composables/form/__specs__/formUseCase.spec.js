/**
 * formUseCase.jsのテスト
 */
import { describe, it, expect, vi } from 'vitest'

vi.mock('@/stores/api/form/apiFormStore')
import { useAPIFormStore, APIFormStore } from '@/stores/api/form/apiFormStore'

import { useFormUseCase, FormUseCase } from '../formUseCase'

describe('useFormUseCase', () => {
  it('FormUseCase を返す', () => {
    const useCase = useFormUseCase()
    expect(useCase).toHaveProperty('getRefs')
    expect(useCase).toHaveProperty('getData')
    expect(useCase).toHaveProperty('fetch')

    expect(useAPIFormStore).toHaveBeenCalled()
  })
})

describe('FormUseCase', () => {
  describe('getRefs', () => {
    it('APIFormStore の storeToRefs を呼び出す', () => {
      const { getRefs } = FormUseCase(APIFormStore)

      getRefs()
      expect(APIFormStore.storeToRefs).toHaveBeenCalled()
    })
  })

  describe('getData', () => {
    it('APIFormStore の data を返す', () => {
      const { getData } = FormUseCase(APIFormStore)

      const data = getData()
      expect(data).toBe(APIFormStore.data)
    })
  })

  describe('fetch', () => {
    it('APIFormStore の fetch を呼び出す', async () => {
      const { fetch } = FormUseCase(APIFormStore)

      APIFormStore.fetch.mockResolvedValue(true)
      await fetch()

      expect(APIFormStore.fetch).toHaveBeenCalled()
    })

    it.skip('エラー時は (決まってない)', async () => {
      const { fetch } = FormUseCase(APIFormStore)

      APIFormStore.fetch.mockRejectedValue(new Error('error'))
      const result = await fetch()

      expect(result).toBe(false)
    })
  })
})
