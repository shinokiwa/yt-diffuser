/**
 * プレビュー関連の処理をまとめたコンポーザブル
 */
import { ref, onMounted, onUnmounted } from 'vue'
import { useApi } from '@/composables/api'

const previewSrc = ref ("")

export function useOutputPreview() {
    let source
    onMounted(() => {
        source = new EventSource('/api/res/output/preview')
        source.onmessage = (event) => {
            if (event.data.length > 0) {
                const data = JSON.parse(event.data)
                previewSrc.value = "output/preview/" +  data.target + '?cacheBuster=' + new Date().getTime()
            }
        }
    })

    onUnmounted(() => {
        if (source && source.readyState !== EventSource.CLOSED) {
            source.close()
        }
    })

    return {
        previewSrc
    }
}