/**
 * 画像ビューワーの状態管理
 */
import { ref } from 'vue'

const isShowViewer = ref(false)
const imageUrl = ref("")

const nextCallback = ref(null)
const prevCallback = ref(null)
const deleteCallback = ref(null)


/**
 * 画像ビューアーを表示する。
 * @returns null
 */
function showViewer(url, next, prev, del) {
    imageUrl.value = url
    nextCallback.value = next
    prevCallback.value = prev
    deleteCallback.value = del
    isShowViewer.value = true
}

/**
 * 画像ビューアーを非表示にする。
 * @returns null
 */
function hideViewer() {
    isShowViewer.value = false
}

/**
 * 画像ビューアーの状態管理
 * @returns {Object} 画像ビューアーの状態管理
 */
export function useViewerStore() {
    return {
        showViewer,
        hideViewer,

        isShowViewer,
        imageUrl,
        nextCallback,
        prevCallback,
        deleteCallback
    }
}
