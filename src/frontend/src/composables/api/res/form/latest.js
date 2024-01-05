/**
 * 最新のフォームデータを取得・更新するAPI
 */
import { useApi } from '@/composables/api'
import { useForm } from '@/composables/store/form'

const { get, post } = useApi()


async function getLatestForm () {
    const { prompt, nPrompt } = useForm()
    const response = await get('/api/res/form/latest')
    const data = await response.json()
    prompt.value = data.prompt
    nPrompt.value = data.n_prompt
}

async function updateLatestForm () {
    const { prompt, nPrompt } = useForm()

    await post ('/api/res/form/latest', {
        prompt: prompt.value,
        n_prompt: nPrompt.value
    })
}

export function useLatestForm () {
    return {
        getLatestForm,
        updateLatestForm
    }
}