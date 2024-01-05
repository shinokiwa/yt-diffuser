/**
 * フォームの状態を管理する
 */
import { ref } from 'vue'

const prompt = ref(null)
const nPrompt = ref(null)


export function useForm() {
    return {
        prompt,
        nPrompt
    }
}