/**
 * 通知の状態管理
 */
import { ref } from 'vue'

/**
 * 通知リスト
 */
const notificationList = ref([])

/**
 * トーストのキュー
 */
const toastQueue = ref([])

export function useNotificationStore() {
    return {
        notification: {
            /**
             * 通知リストを取得する
             * 
             * @returns {Ref} 通知リスト
             */
            getList: () => {
                return notificationList
            },

            /**
             * 通知リストに追加する
             * 
             * @param {string} message 
             */
            add: (message) => {
                notificationList.value.push(message)
            },

            /**
             * 通知リストから指定したインデックスの内容を削除する
             * 
             * @param {number} index
             */
            remove: (index) => {
                notificationList.value.splice(index, 1)
            },

            /**
             * 通知リストをクリアする
             */
            clear: () => {
                notificationList.value = []
            },
        },
        toast: {
            /**
             * トーストキューを取得する
             * 
             * @returns {Ref} トーストキュー
             */
            getQueue: () => {
                return toastQueue
            },

            /**
             * トーストキューを追加する
             * 
             * @param {string} message 追加するメッセージ
             * @param {boolean} withNotification 通知リストにも追加するか
             */
            put: (message, withNotification = true) => {
                toastQueue.value.push(message)
                if (withNotification) notificationList.value.push(message)
            },

            /**
             * トーストキューから最初の要素を取り出す
             */
            get: () => {
                return toastQueue.value.shift()
            },
        },
    }
}