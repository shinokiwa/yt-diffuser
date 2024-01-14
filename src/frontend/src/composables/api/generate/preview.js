/**
 * /api/generate/preview に関する処理をまとめたコンポーザブル
 */
import { ref } from 'vue'
import { useApi } from '@/composables/api'
const { get, post } = useApi()

/**
 * プレビュー画像を生成する
 */
async function start_generate (
    seed,
    width,
    height,
    prompt,
    negative_prompt,
    scheduler,
    inference_steps,
    guidance_scale
) {
    await post('/api/generate/preview/text_to_image', {
        seed: seed,
        width: width,
        height: height,
        prompt: prompt,
        negative_prompt: negative_prompt,
        scheduler: scheduler,
        inference_steps: inference_steps,
        guidance_scale: guidance_scale
    })
}


export function useGeneratePreview () {
    return {
        start_generate
    }
}