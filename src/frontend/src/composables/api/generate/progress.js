/**
 * 生成ワーカーの進捗を取得するコンポーザブル
 */
import { ref } from 'vue'

const generateTotal = ref(0)
const generateCount = ref(0)
const stepsTotal = ref(0)
const stepsCount = ref(0)
const percentage = ref(0)
const elapsed = ref(0)
const remaining = ref(0)
const average = ref(0)

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

export function useGenerateProgress() {
    if (eventSource === null) {
        eventSource = new EventSource('/api/generate/progress')
        eventSource.onmessage = (event) => {
            if (event.data.length > 0) {
                const data = JSON.parse(event.data)
                generateTotal.value = data.generate_total
                generateCount.value = data.generate_count
                stepsTotal.value = data.steps_total
                stepsCount.value = data.steps_count
                percentage.value = data.percentage
                elapsed.value = data.elapsed
                remaining.value = data.remaining
                average.value = data.average
            }
        }
    }

    return {
        generateTotal,
        generateCount,

        stepsTotal,
        stepsCount,

        percentage,
        elapsed,
        remaining,
        average,

        eventSource,
        close
    }
}