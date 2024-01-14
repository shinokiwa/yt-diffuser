/**
 * モデル関連の処理をまとめたコンポーザブル
 */
import { ref } from 'vue'
import { useApi } from '@/composables/api'

const modelList = ref([])

const { get } = useApi()

/**
 * モデル一覧を取得する。
 * 取得結果はallModelsに格納される。
 * 
 * @returns {Promise<void>}
 */
async function getModels () {
    const response = await get('/api/res/model')
    const data = await response.json()
    const list = (data.models || []).sort((a, b) => {
        // model_class、model_nameの順でソートする
        const order = ['base-model', 'lora-model', 'controlnet-model']
        const aIndex = order.indexOf(a.model_class)
        const bIndex = order.indexOf(b.model_class)
        if (aIndex < bIndex) return -1
        if (aIndex > bIndex) return 1
        if (a.model_name < b.model_name) return -1
        if (a.model_name > b.model_name) return 1
        return 0
    })
    modelList.value = list
}

export function useModel() {
    return {
        modelList,
        getModels
    }
}