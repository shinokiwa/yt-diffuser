/**
 * モデル関連の処理をまとめたコンポーザブル
 */
import { ref } from 'vue'
import { useApi } from '@/composables/api'

const allModels = ref([])

const { get } = useApi()

/**
 * モデル一覧を取得する
 */
async function getModels () {
    const response = await get('/api/res/model')
    const list = await response.json()
    allModels.value = list.models || []
    // idを追加
    allModels.value.forEach((model, index) => {
        model.id = index
    })
}

export function useModel() {
    return {
        allModels,
        getModels
    }
}