/**
 * 通知の状態管理
 */
import { ref } from 'vue'

/**
 * 通知エリア表示状態
 */
const notificationState = ref(false)

/**
 * 通知エリアを表示する
 */
function showNotificationArea() {
    notificationState.value = true
}

/**
 * 通知エリアを非表示にする
 */
function hideNotificationArea() {
    notificationState.value = false
}

/**
 * 通知エリアの表示状態を切り替える
 */
function toggleNotificationArea() {
    notificationState.value = !notificationState.value
}

/**
 * 新規の通知キュー
 */
const newNotifications = ref([])

/**
 * 通知を追加する
 * @param {string} message
 */
function addNewNotification(message) {
    newNotifications.value.push(message)
}

/**
 * 通知をクリアする
 */
function clearNewNotifications() {
    return newNotifications.value = []
}

export function useNotificationStore() {
    return {
        notificationState,
        showNotificationArea,
        hideNotificationArea,
        toggleNotificationArea,
        newNotifications,
        addNewNotification,
        clearNewNotifications
    }
}