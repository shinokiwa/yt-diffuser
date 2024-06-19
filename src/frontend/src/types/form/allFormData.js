/**
 * 全フォームデータを保持するクラス
 */
export class AllFormData {
  constructor(data) {
    this.baseModelID = ''
    this.baseModelRevision = ''
    this.compile = 0

    this.loraModelID = ''
    this.loraModelRevision = ''
    this.loraModelWeight = ''

    this.controlnetModelID = ''
    this.controlnetModelRevision = ''
    this.controlnetModelWeight = ''

    this.seed = null
    this.generateType = 't2i'

    this.width = 1024
    this.height = 1024

    this.strength = 0.3

    this.prompt = ''
    this.negativePrompt = ''
    this.scheduler = 'ddim'
    this.inferenceSteps = 30
    this.guidanceScale = 8.0

    this.memo = ''

    if (data) {
      this.setData(data)
    }
  }

  setData(data) {
    this.baseModelID = data.baseModelID
    this.baseModelRevision = data.baseModelRevision
    this.compile = data.compile

    this.loraModelID = data.loraModelID
    this.loraModelRevision = data.loraModelRevision
    this.loraModelWeight = data.loraModelWeight

    this.controlnetModelID = data.controlnetModelID
    this.controlnetModelRevision = data.controlnetModelRevision
    this.controlnetModelWeight = data.controlnetModelWeight

    this.seed = data.seed
    this.generateType = data.generateType

    this.width = data.width
    this.height = data.height

    this.strength = data.strength

    this.prompt = data.prompt
    this.negativePrompt = data.negativePrompt
    this.scheduler = data.scheduler
    this.inferenceSteps = data.inferenceSteps
    this.guidanceScale = data.guidanceScale

    this.memo = data.memo
  }
}
