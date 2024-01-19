/**
 * プロンプトを保存、取得するAPI
 */
import { useApi } from '@/composables/api'

const { get, post } = useApi()

/**
 * プロンプトを保存する
 * 
 * @param {String} prompt プロンプト
 */
async function savePrompt (prompt) {
    const response = await post('/api/res/form/prompt', { prompt })
    return response
}

/**
 * ネガティブプロンプトを保存する
 * 
 * @param {String} prompt プロンプト
 */
async function saveNegativePrompt (prompt) {
    const response = await post('/api/res/form/negative_prompt', { prompt })
    return response
}

export function useFormPrompt () {
    return {
        savePrompt,
        saveNegativePrompt
    }
}
