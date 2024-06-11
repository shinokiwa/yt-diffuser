/**
 * /api/generate/image に関する処理をまとめたコンポーザブル
 */
import { useAPI } from '@/adapters/api'
import { useFormStore } from '@/stores/form/formStore'

/**
 * 生成ユースケースを返す
 */
export function useGenerateUseCase() {
  return GenerateUseCase(useFormStore(), useAPI())
}

export function GenerateUseCase(store, api) {
  return {
    /**
     * Text to Image で画像を生成する。
     * 基本的にフォームストアの内容を使ってリクエストを送信する。
     */
    async text_to_image(count) {
      try {
        await api.post('/api/generate/text_to_image', {
          generate_count: count,
          prompt: store.data.prompt,
          negative_prompt: store.data.negativePrompt,
          scheduler: store.data.scheduler
        })
      } catch (e) {
        console.error(e)
      }
    }
  }
}
