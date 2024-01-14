/**
 * /api/generate/process に関する処理をまとめたコンポーザブル
 */
import { ref } from 'vue'
import { useApi } from '@/composables/api'
const { get, post } = useApi()


/**
 * モデルをロードする
 */
async function loadModel (model_name, revision) {
    await post('/api/generate/process/load', {
        model_name,
        revision
    })
}

/**
 * モデルを解放する
 */
async function removeModel () {
    await get('/api/generate/process/terminate')
}

/**
 * LoRAを解放する
 */
async function removeLora () {
    await get('/api/generate/process/lora/remove')
}



export function useGenerateProcess () {
    return {
        loadModel,
        removeModel,
        removeLora,
    }
}