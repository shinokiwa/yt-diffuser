/**
 * サーバー情報のユースケース コンポーザブル
 */
import { ref } from 'vue'
import { useServerStatusStore } from '@/stores/server/statusStore'
import { useAPI } from '@/adapters/api'

/**
 * サーバー情報ユースケースを返す
 * @returns {ReturnType<typeof ServerStatusUseCase>}
 */
export function useServerStatusUseCase() {
  return ServerStatusUseCase(useServerStatusStore(), useAPI())
}

/**
 * サーバー情報ユースケース
 *
 * @param {ReturnType<typeof useHealthStore>} store
 * @param {ReturnType<typeof useAPI>} api
 */
export function ServerStatusUseCase(store, api) {
  const connected = store.refs.isConnected
  const disconnected = ref(false)

  async function check() {
    try {
      const response = await api.get('/api/server/status')

      return response.health === 'ok'
    } catch (e) {
      return false
    }
  }

  async function timer() {
    const result = await check()
    if (result) {
      store.connected()
      setTimer(30000)
    } else if (store.isConnected) {
      disconnected.value = true
      return
    } else {
      setTimer(5000)
    }
  }

  /**
   * ヘルスチェックタイマー
   *
   * @param {number} nextTime 次回実行までの時間
   */
  function setTimer(nextTime) {
    store.setTimer(setTimeout(timer, nextTime))
  }

  return {
    connected,
    disconnected,

    /**
     * 定期的なヘルスチェック開始
     *
     * @returns {Promise<Boolean>} ヘルスチェック結果 OKならtrue
     */
    open: () => {
      if (store.timer === null) {
        timer()
      }
    },

    close: () => {
      clearTimeout(store.timer)
      store.setTimer(null)
    }
  }
}
