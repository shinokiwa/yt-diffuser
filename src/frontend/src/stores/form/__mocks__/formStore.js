/**
 * apiFormStore.js のモック
 */
import { vi } from 'vitest'
import { toRefs } from 'vue'

export const FormStore = {
  data: {
    baseModelName: '',
    baseModelRevision: '',
    compile: 0,

    loraModelName: '',
    loraModelRevision: '',
    loraModelWeight: '',

    controlnetModelName: '',
    controlnetModelRevision: '',
    controlnetModelWeight: '',

    seed: 0,
    generateType: 't2i',

    width: 1024,
    height: 1024,

    strength: 0.3,

    prompt: '',
    negativePrompt: '',
    scheduler: 'ddim',
    inferenceSteps: 30,
    guidanceScale: 8.0,

    memo: ''
  },
  get refs() {
    return vi.fn().mockReturnValue(toRefs(this.data))
  }
}

export const useFormStore = vi.fn().mockReturnValue(FormStore)
