/**
 * フォームの状態を管理する。
 * 
 * フォーム入力値は画面をまたいで保持する必要があるため、
 * コンポーザブルで状態管理する。
 */
import { ref } from 'vue'

const baseModelName = ref("")
const baseModelRevision = ref("")
const compile = ref(0)

const loraModelName = ref("")
const loraModelRevision = ref("")
const loraModelWeight = ref("")

const controlnetModelName = ref("")
const controlnetModelRevision = ref("")
const controlnetModelWeight = ref("")

const seed = ref(0)
const generateType = ref("t2i")

const width = ref(1024)
const height = ref(1024)

const strength = ref(0.3)

const prompt = ref("")
const negativePrompt = ref("")
const scheduler = ref("ddim")
const inferenceSteps = ref(30)
const guidanceScale = ref(8.0)

const memo = ref("")

export function useFormStore() {
    return {
        baseModelName,
        baseModelRevision,
        compile,

        loraModelName,
        loraModelRevision,
        loraModelWeight,

        controlnetModelName,
        controlnetModelRevision,
        controlnetModelWeight,

        seed,
        generateType,

        height,
        width,

        prompt,
        negativePrompt,
        scheduler,
        inferenceSteps,
        guidanceScale,

        strength,

        memo
    }
}