/**
 * 生成ワーカーの状態を取得するコンポーザブル
 */
import { ref } from 'vue'

import { useToastStore } from '@/composables/store/toast'
const { putToastQueue } = useToastStore()

const status = ref('') 
const baseModelLabel = ref('')
const loraModelLabel = ref('')
const controlnetModelLabel = ref('')

let eventSource = null

/**
 * 接続を閉じる
 */
export function close() {
    if (eventSource !== null) {
        eventSource.close()
        eventSource = null
    }
}

export function useGenerateStatus() {
    if (eventSource === null) {
        eventSource = new EventSource('/api/generate/status')
        eventSource.onmessage = (event) => {
            if (event.data.length > 0) {
                const data = JSON.parse(event.data)
                if (!data.status) {
                    data.status = ''
                }

                if (data.status === '' || data.status === 'exit') {
                    status.value = 'empty'
                    putToastQueue('アイドル状態', false)
                } else if (data.status === 'loading') {
                    status.value = 'loading'
                    putToastQueue('モデル読み込み中...', false)
                } else if (data.status === 'ready') {
                    status.value = 'ready'
                    putToastQueue('生成準備完了', false)
                } else if (data.status === 'compiling') {
                    status.value = 'compiling'
                    putToastQueue('コンパイル中...', false)
                } else if (data.status === 'generating') {
                    status.value = 'generating'
                    putToastQueue('生成中...', false)
                }

                baseModelLabel.value = data.base_model_label
                loraModelLabel.value = data.lora_model_label
                controlnetModelLabel.value = data.controlnet_model_label
            }
        }
    }

    return {
        status,
        baseModelLabel,
        loraModelLabel,
        controlnetModelLabel,

        eventSource,
        close
    }
}