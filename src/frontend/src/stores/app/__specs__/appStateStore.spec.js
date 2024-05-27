/**
 * appStateStore.js のテスト
 */
import { describe, it, expect } from 'vitest'
import { createApp } from 'vue'
import { setActivePinia, createPinia } from 'pinia'

import { VIEW_IDS } from '@/utils/enum/view'

import { useAppStateStore } from '../appStateStore'

describe('useAppStateStore', () => {
  const app = createApp({})
  const pinia = createPinia()
  app.use(pinia)
  setActivePinia(pinia)

  it('AppStateStore を返す', () => {
    const store = useAppStateStore()
    expect(store).toHaveProperty('currentView')
    expect(store.currentView).toBe(VIEW_IDS.INITIALIZING)
    expect(store).toHaveProperty('changeView')
  })

  describe('changeView', () => {
    it('ビューを変更する', () => {
      const store = useAppStateStore()
      store.changeView(VIEW_IDS.MODEL_MANAGE)
      expect(store.currentView).toBe(VIEW_IDS.MODEL_MANAGE)
    })
  })
})
