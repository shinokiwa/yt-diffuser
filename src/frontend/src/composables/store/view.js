/**
 * ビューの状態を管理する
 */
import { ref } from 'vue'

/**
 * 現在のビュー
 */
const currentView = ref(0)

/**
 * 通知エリア表示状態
 */
const notificationAreaState = ref(false)


export function useViewStore() {
    return {
        /**
         * ビューに関するストア
         */
        view: {
            /**
             * 現在のビューを取得する
             * 
             * @returns {Ref} 現在のビュー
             */
            getCurrent: ()=> {
                return currentView
            },

            /**
             * ビューを切り替える
             * @param {number} view ビュー番号
             */
            change: (view) => {
                currentView.value = view
            },

            /**
             * ビュー番号の定義
             */
            views: {
                INITIALIZING: 0,
                MODEL_MANAGE: 1,
                PROMPT_SETTING: 2,
                GENERATE_BATCH: 3,
                GALLERY: 4,
                EDITOR: 5,
            },
        },

        /**
         * 通知エリアに関するストア
         */
        notificationArea: {
            /**
             * 通知エリアの表示状態を取得する
             * 
             * @returns {Ref} 通知エリアの表示状態
             */
            getState: () => {
                return notificationAreaState
            },

            /**
             * 通知エリアを表示する
             */
            show: () => {
                notificationAreaState.value = true
            },

            /**
             * 通知エリアを非表示にする
             */
            hide: () => {
                notificationAreaState.value = false
            },

            /**
             * 通知エリアの表示状態を切り替える
             */
            toggle: () => {
                notificationAreaState.value = !notificationAreaState.value
            },
        }
    }
}