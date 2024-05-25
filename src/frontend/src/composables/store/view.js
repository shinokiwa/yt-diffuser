/**
 * ビューの状態を管理する
 */
import { ref } from 'vue'

/**
 * ビュー番号の定義
 */
const views = {
    INITIALIZING: 0,
    MODEL_MANAGE: 1,
    PROMPT_SETTING: 2,
    GENERATE_BATCH: 3,
    GALLERY: 4,
    EDITOR: 5,
}

/**
 * 現在のビュー
 */
const currentView = ref(0)

/**
 * ビューを切り替える
 * 
 * @param {number} view ビュー番号
 */
function changeView(view) {
    currentView.value = view
}


export function useViewStore() {
    return {
        views,
        currentView,
        changeView,
    }
}