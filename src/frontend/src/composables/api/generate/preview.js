/**
 * /api/generate/preview に関する処理をまとめたコンポーザブル
 */
import { ref } from 'vue'
import { useApi } from '@/composables/api'
const { get, post } = useApi()

/**
 * プレビュー画像を生成する
 */
async function start_generate (seed, prompt, negative_prompt, inference_steps) {
    await post('/api/generate/preview/text_to_image', {
        seed: seed,
        prompt: prompt,
        negative_prompt: negative_prompt,
        inference_steps: inference_steps
    })
}


export function useGeneratePreview () {
    return {
        start_generate
    }
}