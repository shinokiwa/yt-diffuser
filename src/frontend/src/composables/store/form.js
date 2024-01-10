/**
 * フォームの状態を管理する
 */
import { ref } from 'vue'

const seed = ref(0)
const prompt = ref("")
const nPrompt = ref("")
const inferenceSteps = ref(30)


export function useForm() {
    return {
        seed,
        prompt,
        nPrompt,
        inferenceSteps
    }
}