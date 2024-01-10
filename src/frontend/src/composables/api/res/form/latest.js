/**
 * 最新のフォームデータを取得・更新するAPI
 */
import { useApi } from '@/composables/api'
import { useForm } from '@/composables/store/form'

const { get, post } = useApi()


async function getLatestForm () {
    const { seed, prompt, nPrompt, inferenceSteps } = useForm()
    const response = await get('/api/res/form/latest')
    const data = await response.json()

    if ("seed" in data) seed.value = parseInt(data.seed)
    if ("prompt" in data) prompt.value = data.prompt
    if ("negative_prompt" in data) nPrompt.value = data.negative_prompt
    if ("inference_steps" in data) inferenceSteps.value = parseInt(data.inference_steps)
}

async function updateLatestForm () {
    const { seed, prompt, nPrompt, inferenceSteps } = useForm()

    await post ('/api/res/form/latest', {
        seed: seed.value,
        prompt: prompt.value,
        negative_prompt: nPrompt.value,
        inference_steps: inferenceSteps.value
    })
}

export function useLatestForm () {
    return {
        getLatestForm,
        updateLatestForm
    }
}