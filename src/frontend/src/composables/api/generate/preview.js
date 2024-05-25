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
    generate_type,
    seed,
    width,
    height,
    prompt,
    negative_prompt,
    scheduler,
    inference_steps,
    guidance_scale,
    strength
) {
    let url = '/api/generate/preview/text_to_image'
    if (generate_type === 'i2i') {
        url = '/api/generate/preview/image_to_image'
    } else if (generate_type === 'inpaint') {
        url = '/api/generate/preview/inpaint'
    }

    await post(url, {
        seed: seed,
        width: width,
        height: height,
        prompt: prompt,
        negative_prompt: negative_prompt,
        scheduler: scheduler,
        inference_steps: inference_steps,
        guidance_scale: guidance_scale,
        strength: strength
    })
}


export function useGeneratePreview () {
    return {
        start_generate
    }
}