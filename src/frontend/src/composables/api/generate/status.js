/**
 * 生成ワーカーの状態を取得するコンポーザブル
 */
import { ref, onMounted, onUnmounted, watch } from 'vue'

import { useNotificationStore } from '@/composables/store/notification';
const { toast } = useNotificationStore()

const status = ref('') 

export function useGenerateStatus() {
    const eventSource = new EventSource('/api/generate/status')
    eventSource.onmessage = (event) => {
        if (event.data.length > 0) {
            const data = JSON.parse(event.data)
            if (!data.status) {
                data.status = ''
            }

            if (data.status === '' || data.status === 'exit') {
                status.value = 'empty'
                toast.put('アイドル状態', false)
            } else if (data.status === 'loading') {
                status.value = 'loading'
                toast.put('モデル読み込み中...', false)
            } else if (data.status === 'ready') {
                status.value = 'ready'
                toast.put('生成準備完了', false)
            } else if (data.status === 'generating') {
                status.value = 'generating'
                toast.put('生成中...', false)
            }
        }
    }

    onUnmounted(() => {
        eventSource.close()
    })

    return {
        status,
        eventSource
    }
}