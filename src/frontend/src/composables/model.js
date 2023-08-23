/**
 * モデル関連の処理をまとめたコンポーザブル
 */
import { ref } from 'vue'
import { useApi } from '@/composables/api'

const baseModels = ref([])
const loraModels = ref([])
const upscaleModels = ref([])

const { api } = useApi()

async function loadModels () {
    const response = await api.get('/api/model')
    const list = response.data
    baseModels.value = list.base || []
    loraModels.value = list.lora || []
    upscaleModels.value = list.upscale || []
}

export function useModel() {
    return {
        baseModels,
        loraModels,
        upscaleModels,

        loadModels
    }
}