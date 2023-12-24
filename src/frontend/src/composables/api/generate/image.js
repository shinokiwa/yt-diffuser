/**
 * /api/generate/image に関する処理をまとめたコンポーザブル
 */
import { ref } from 'vue'
import { useApi } from '@/composables/api'
const { get, post } = useApi()


/**
 * モデルをロードする
 */
async function loadModel (model_name, revision) {
    await post('/api/generate/image/load', {
        model_name,
        revision
    })
}


/**
 * 画像を生成する
 */
async function start_generate (prompt) {
    await post('/api/generate/image/generate', {
        text: prompt
    })
}


export function useGenerateImage () {
    return {
        loadModel,
        start_generate
    }
}