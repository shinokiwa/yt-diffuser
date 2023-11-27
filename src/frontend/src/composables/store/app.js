/**
 * アプリ全体に関するストア
 */
import { ref } from 'vue'

/**
 * ローディング状態
 */
const readyState = ref(false)

/**
 * ローディング完了
 */
function ready () {
    readyState.value = true
}

export function useAppStore() {
    return {
        readyState,
        ready
    }
}
