/**
 * サーバーからのメッセージを受信するコンポーザブル
 */
import { ref } from 'vue'

import { useNotificationStore } from '@/composables/store/notification';
const { addNewNotification } = useNotificationStore()

/**
 * メッセージ受信を開始する
 * 
 * @return EventSource
 */
function openMessage () {
    const source = new EventSource('/api/sse/message')
    source.onmessage = (event) => {
        if (event.data.length > 0) {
            const data = JSON.parse(event.data)
            addNewNotification(data.label)
        }
    }

    return source
}

export function useMessage() {
    return {
        openMessage
    }
}