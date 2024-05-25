/**
 * トーストキューの管理
 */
import { ref } from 'vue'

import { useNotificationStore } from '@/composables/store/notification'

/**
 * トーストのキュー
 */
const toastQueue = ref([])

/**
 * トーストキューを追加する
 * 
 * @param {string} message 追加するメッセージ
 * @param {boolean} withNotification 通知リストにも追加するか
 */
function putToastQueue (message, withNotification = false) {
    const { notificationList } = useNotificationStore()

    toastQueue.value.push(message)
    if (withNotification) notificationList.value.push(message)
}

/**
 * トーストキューから最初の要素を取り出す
 */
function getToastQueue () {
    return toastQueue.value.shift()
}

export function useToastStore() {
    return {
        toastQueue,
        putToastQueue,
        getToastQueue,
    }
}