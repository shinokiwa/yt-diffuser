/**
 * apiHealthStore.js のモック
 */
import { vi } from 'vitest'
import { ref } from 'vue'

const ServerStatusStore = (() => {
  return {
    data: {
      health: 'ng',
      downloader: 'idle',
      generator: 'idle'
    },
    isConnected: false,
    timer: null,
    get refs() {
      return {
        isConnected: ref(this.connected)
      }
    },
    setStatus: vi.fn((status) => {
      this.data.health = status?.health
      this.data.downloader = status?.downloader
      this.data.generator = status?.generator
    }),
    setTimer: vi.fn()
  }
})()

export const useServerStatusStore = vi.fn().mockReturnValue(ServerStatusStore)
