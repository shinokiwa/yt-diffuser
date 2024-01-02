/**
 * ビューの状態を管理する
 */
import { ref } from 'vue'

/**
 * 現在のビュー
 */
const currentView = ref(0)

function changeView(view) {
    currentView.value = view
}


export function useViewStore() {
    return {
        currentView,
        changeView,

        // ビューの定義
        INITIALIZING: 0,
        MODEL_MANAGE: 1,
        PROMPT_SETTING: 2,
        GENERATE_BATCH: 3,
        GALLERY: 4,
        EDITOR: 5,
    }
}