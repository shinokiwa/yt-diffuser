/**
 * サーバーからのイベントを処理するユースケース
 */
import { onMounted, onUnmounted, ref } from 'vue'

import { useAPI } from '@/adapters/api'

export function useServerEventUseCase() {
  return ServerEventUseCase(useAPI())
}

/**
 * サーバーからのイベントを処理するユースケース
 *
 * @param {ReturnType<typeof useAPI>} api
 */
export function ServerEventUseCase(api) {
  let source = null

  onMounted(() => {
    source = new EventSource('/api/server/event')
    source.onmessage = (event) => {
      console.log(event.data)
    }
  })

  onUnmounted(() => {
    if (source) {
      source.close()
    }
  })

  return {}
}
