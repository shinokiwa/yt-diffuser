/**
 * ワーカープロセスのステータスを取得し保持するストアコンポーザブル
 */
import { ref } from 'vue'

const status = ref('')

let sseSource = null

/**
 * SSEを開始する
 */
function startSse () {
    sseSource = new EventSource('/api/sse/status')
    sseSource.onmessage = (event) => {
        const data = event.data
        status.value = data
    }
}

export function useStatusStore() {
    if (sseSource == null || sseSource.readyState == 2) {
        startSse()
    }

    return {
        status
    }
}