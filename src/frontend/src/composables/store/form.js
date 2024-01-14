/**
 * フォームの状態を管理する。
 * 
 * フォーム入力値は画面をまたいで保持する必要があるため、
 * コンポーザブルで状態管理する。
 */
import { ref } from 'vue'

const baseModel = ref("")
const baseModelRevision = ref("")

const loraModel = ref("")
const loraModelRevision = ref("")
const loraModelWeight = ref("")

const controlnetModel = ref("")
const controlnetModelRevision = ref("")
const controlnetModelWeight = ref("")

const seed = ref(0)
const width = ref(1024)
const height = ref(1024)

const prompt = ref("")
const negativePrompt = ref("")
const scheduler = ref("ddim")
const inferenceSteps = ref(30)
const guidanceScale = ref(8.0)

const memo = ref("")

export function useFormStore() {
    return {
        baseModel,
        baseModelRevision,

        loraModel,
        loraModelRevision,
        loraModelWeight,

        controlnetModel,
        controlnetModelRevision,
        controlnetModelWeight,

        seed,
        height,
        width,

        prompt,
        negativePrompt,
        scheduler,
        inferenceSteps,
        guidanceScale,

        memo
    }
}