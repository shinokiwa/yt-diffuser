/**
 * モデル関連の処理をまとめたコンポーザブル
 */
import { ref } from 'vue'
import { useApi } from '@/composables/api'

const baseModels = ref([])
const loraModels = ref([])
const controlnetModels = ref([])

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

    const base = []
    const lora = []
    const controlnet = []

    if (data?.models) {
        data.models.forEach(el => {
            if (el.model_class === 'base-model') {
                base.push(el)
            } else if (el.model_class === 'lora-model') {
                lora.push(el)
            } else if (el.model_class === 'controlnet-model') {
                controlnet.push(el)
            }
        });

        // それぞれモデル名でソート
        function sortModelName (a, b) {
            if (a.model_name < b.model_name) {
                return -1
            } else {
                return 1
            }
        }
        base.sort(sortModelName)
        lora.sort(sortModelName)
        controlnet.sort(sortModelName)
    }

    baseModels.value = base
    loraModels.value = lora
    controlnetModels.value = controlnet
}

export function useModel() {
    return {
        baseModels,
        loraModels,
        controlnetModels,

        getModels
    }
}