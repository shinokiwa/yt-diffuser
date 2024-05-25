/**
 * ワーカープロセスの進捗状態を取得し保持するストアコンポーザブル
 */
import { ref } from 'vue'

const progress = ref('')

let sseSource = null

/**
 * SSEを開始する
 */
function startSse () {
    sseSource = new EventSource('/api/sse/progress')
    sseSource.onmessage = (event) => {
        const data = event.data
        progress.value = data
    }
}

export function useProgressStore() {
    if (sseSource == null || sseSource.readyState == 2) {
        startSse()
    }

    return {
        progress
    }
}