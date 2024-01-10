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
async function start_generate (
    generate_count,
    prompt,
    negative_prompt,
    inference_steps
) {
    await post('/api/generate/image/text_to_image', {
        generate_count: generate_count,
        prompt: prompt,
        negative_prompt: negative_prompt,
        inference_steps: inference_steps
    })
}


export function useGenerateImage () {
    return {
        loadModel,
        start_generate
    }
}