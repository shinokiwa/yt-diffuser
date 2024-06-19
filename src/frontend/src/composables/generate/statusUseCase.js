import { onMounted, onUnmounted } from 'vue'
import { useAppStateStore, useLogStore } from '@/stores/app'

export function useGenerateStatusEventUseCase() {
  return GenerateStatusEventUseCase(useAppStateStore(), useLogStore())
}

/**
 * 生成ステータスのイベントを処理するユースケース
 *
 * @param {ReturnType<typeof useAppStateStore>} appStateStore
 * @param {ReturnType<typeof useLogStore>} logStore
 */
export function GenerateStatusEventUseCase(appStateStore, logStore) {
  let source = null

  onMounted(() => {
    source = new EventSource('/api/generate/status')

    source.onopen = () => {
      appStateStore.isConnected = true
    }

    source.onmessage = (event) => {
      logStore.addLog(event.data, true)
    }
  })

  onUnmounted(() => {
    if (source) {
      source.close()
    }
  })

  return {}
}
