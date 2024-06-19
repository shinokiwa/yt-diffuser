import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'

import { useLogStore } from '../logStore'

describe('useLogStore', () => {
  const pinia = createPinia()
  setActivePinia(pinia)

  beforeEach(() => {
    const store = useLogStore()
    store.$reset()
  })

  describe('addLog', () => {
    it('ログを追加する。', () => {
      const store = useLogStore()
      store.addLog('test')
      expect(store.logs).toEqual(['test'])
    })

    it('トーストを追加する。', () => {
      const store = useLogStore()
      store.addLog('test', true)
      expect(store.logs).toEqual(['test'])
      expect(store.toast).toEqual(['test'])
    })
  })

  describe('clearLog', () => {
    it('ログをクリアする。', () => {
      const store = useLogStore()
      store.addLog('test')
      store.clearLog()
      expect(store.logs).toEqual([])
    })
  })

  describe('getToast', () => {
    it('トーストを取得する。取得したトーストは除去される。', () => {
      const store = useLogStore()
      store.addLog('test', true)
      expect(store.getToast()).toBe('test')
      expect(store.logs).toEqual(['test'])
      expect(store.toast).toEqual([])
    })
  })
})
