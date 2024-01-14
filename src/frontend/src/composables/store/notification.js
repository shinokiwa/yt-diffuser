/**
 * 通知の状態管理
 */
import { ref } from 'vue'

/**
 * 通知リスト
 */
const notificationList = ref([])

/**
 * 通知リストに追加する
 * 
 * @param {string} message 
 */
function addNotification (message) {
    notificationList.value.push(message)
}

/**
 * 通知リストから指定したインデックスの内容を削除する
 * 
 * @param {number} index
 */
function removeNotification (index) {
    notificationList.value.splice(index, 1)
}

/**
 * 通知リストをクリアする
 */
function clearNotification () {
    notificationList.value = []
}


export function useNotificationStore() {
    return {
        notificationList,
        addNotification,
        removeNotification,
        clearNotification,
    }
}