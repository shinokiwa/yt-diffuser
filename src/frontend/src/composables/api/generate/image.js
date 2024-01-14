/**
 * /api/generate/image に関する処理をまとめたコンポーザブル
 */
import { useApi } from '@/composables/api'
const { post } = useApi()


/**
 * 画像を生成する
 */
async function start_generate (
    generate_count,
    width,
    height,
    prompt,
    negative_prompt,
    scheduler,
    inference_steps,
    guidance_scale
) {
    await post('/api/generate/image/text_to_image', {
        generate_count: generate_count,
        width: width,
        height: height,
        prompt: prompt,
        negative_prompt: negative_prompt,
        scheduler: scheduler,
        inference_steps: inference_steps,
        guidance_scale: guidance_scale
    })
}


export function useGenerateImage () {
    return {
        start_generate
    }
}