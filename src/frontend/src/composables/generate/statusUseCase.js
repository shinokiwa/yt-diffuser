import { toRef, onMounted, onUnmounted } from 'vue'
import { toCamelCase } from '@/adapters/api/convert'
import { useAppStateStore, useLogStore } from '@/stores/app'
import { useGenerateProgressStore } from '@/stores/generate/progressStore'

export function useGenerateStatusEventUseCase() {
  return GenerateStatusEventUseCase(useAppStateStore(), useLogStore(), useGenerateProgressStore())
}

/**
 * 生成ステータスのイベントを処理するユースケース
 *
 * @param {ReturnType<typeof useAppStateStore>} appStateStore
 * @param {ReturnType<typeof useLogStore>} logStore
 * @param {ReturnType<typeof useGenerateProgressStore>} progressStore
 */
export function GenerateStatusEventUseCase(appStateStore, logStore, progressStore) {
  let source = null
  let lastStatus = 'IDLE'

  onMounted(() => {
    source = new EventSource('/api/generate/status')

    source.onopen = () => {
      appStateStore.isConnected = true
    }

    source.onmessage = (event) => {
      const data = toCamelCase(JSON.parse(event.data))
      if (data.status !== lastStatus) {
        if (data.status === 'LOADING') {
          logStore.addLog('モデル読み込み中', true)
        } else if (data.status === 'LOADED') {
          logStore.addLog('モデル読み込み完了', true)
        } else if (data.status === 'PROCESSING') {
          logStore.addLog('生成中', true)
        } else if (data.status === 'COMPLETED') {
          logStore.addLog('生成完了', true)
        }
        lastStatus = data.status
      }

      if (data.status === 'PROCESSING') {
        progressStore.setProgress(data)
      }
    }
  })

  onUnmounted(() => {
    if (source) {
      source.close()
    }
  })

  return {
    getRefs: () => ({
      generateTotal: toRef(progressStore, 'generateTotal'),
      generateCount: toRef(progressStore, 'generateCount'),

      percentage: toRef(progressStore, 'percentage'),
      elapsed: toRef(progressStore, 'elapsed'),
      remaining: toRef(progressStore, 'remaining'),
      average: toRef(progressStore, 'average')
    })
  }
}
