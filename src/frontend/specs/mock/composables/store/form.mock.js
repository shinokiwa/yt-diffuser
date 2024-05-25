/**
 * composables/store/form.js のモック
 */
import { ref } from 'vue'

const mockObj = {
    prompt: ref(''),
    negativePrompt: ref('')
}

export function useFormStoreMock() {
    return mockObj
}

