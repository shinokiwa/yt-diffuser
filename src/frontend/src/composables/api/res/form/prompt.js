/**
 * プロンプトを保存、取得するAPI
 */
import { useApi } from '@/composables/api'

const { get, post, del } = useApi()

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
 * プロンプトを取得する
 */
async function getPrompt () {
    const response = await get('/api/res/form/prompt')
    const data = await response.json()
    return data.prompts
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

/**
 * ネガティブプロンプトを取得する
 */
async function getNegativePrompt () {
    const response = await get('/api/res/form/negative_prompt')
    const data = await response.json()
    return data.prompts
}

/**
 * プロンプトを削除する
 */
async function deletePrompt (id) {
    const response = await del(`/api/res/form/prompt/${id}`)
    return response
}


export function useFormPrompt () {
    return {
        savePrompt,
        getPrompt,
        saveNegativePrompt,
        getNegativePrompt,
        deletePrompt
    }
}
