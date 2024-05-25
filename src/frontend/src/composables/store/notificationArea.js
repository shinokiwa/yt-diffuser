/**
 * 通知エリアの表示状態を管理する
 */
import { ref } from 'vue'

/**
 * 通知エリア表示状態
 */
const notificationAreaState = ref(false)

/**
 * 通知エリアを表示する
 */
function show() {
    notificationAreaState.value = true
}

/**
 * 通知エリアを非表示にする
 */
function hide() {
    notificationAreaState.value = false
}

/**
 * 通知エリアの表示状態を切り替える
 */
function toggle() {
    notificationAreaState.value = !notificationAreaState.value
}

export function useNotificationAreaStore() {
    return {
        notificationAreaState,
        show,
        hide,
        toggle,
    }
}
