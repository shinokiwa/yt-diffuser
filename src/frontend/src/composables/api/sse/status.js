/**
 * サーバーステータスをSSEで取得するコンポーザブル
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

export function useStatus() {
    if (sseSource == null || sseSource.readyState == 2) {
        startSse()
    }

    return {
        status
    }
}