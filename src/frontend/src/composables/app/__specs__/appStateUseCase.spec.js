/**
 * appStateUseCase.js のテスト
 */
import { describe, it, expect, vi } from 'vitest'

vi.mock('@/stores/app/appStateStore')
import { useAppStateStore, AppStateStore } from '@/stores/app/appStateStore'

import { VIEW_IDS } from '@/utils/enum/view'

import { useAppStateUseCase, AppStateUseCase } from '../appStateUseCase'

describe('useAppStateUseCase', () => {
  it('AppStateUseCase を返す', () => {
    const useCase = useAppStateUseCase()
    expect(useCase).toHaveProperty('getRefs')

    expect(useAppStateStore).toHaveBeenCalled()
  })
})

describe('AppStateUseCase', () => {
  describe('getRefs', () => {
    it('リアクティブなフロントエンド状態を取得する', () => {
      const useCase = AppStateUseCase(AppStateStore)

      const refs = useCase.getRefs()
      const refsMock = AppStateStore.refs
      expect(refs).toEqual(refsMock)
    })
  })

  describe('changeView', () => {
    it('ビューを変更する', () => {
      const useCase = AppStateUseCase(AppStateStore)

      useCase.changeView(VIEW_IDS.EDITOR)
      expect(AppStateStore.changeView).toHaveBeenCalled()
      expect(AppStateStore.changeView).toHaveBeenCalledWith(VIEW_IDS.EDITOR)
    })
  })
})
