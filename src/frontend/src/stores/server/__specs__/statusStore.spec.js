/**
 * statusStore.js のテスト
 *
 */
import { describe, it, expect } from 'vitest'
import { isRef } from 'vue'
import { setActivePinia, createPinia } from 'pinia'

import { useServerStatusStore } from '../statusStore'

describe('useServerStatusStore', () => {
  const pinia = createPinia()
  setActivePinia(pinia)

  describe('refs', () => {
    it('refs を返す', () => {
      const store = useServerStatusStore()
      const refs = store.refs

      expect(isRef(refs.isConnected)).toBe(true)
    })
  })

  describe('setStatus', () => {
    it('サーバーステータスを更新する', () => {
      const store = useServerStatusStore()
      store.setStatus({ health: 'ok', downloader: 'idle', generator: 'idle' })

      expect(store.data.health).toBe('ok')
      expect(store.data.downloader).toBe('idle')
      expect(store.data.generator).toBe('idle')
    })
  })

  describe('connected', () => {
    it('接続済みにする', () => {
      const store = useServerStatusStore()
      store.connected()

      expect(store.isConnected).toBe(true)
    })
  })

  describe('setTimer', () => {
    it('タイマーを保持する。', async () => {
      const store = useServerStatusStore()

      // タイマーを保持する用途ではあるが、特に値を制限しているわけではないので、
      // 任意の値を設定しても不具合はない。
      store.setTimer(30000)
      expect(store.timer).toEqual(30000)
    })
  })
})
