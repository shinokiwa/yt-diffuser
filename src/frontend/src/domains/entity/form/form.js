import { StringItem } from '@/domains/value/base/stringItem'
import { BoolItem } from '@/domains/value/base/boolItem'
import { FloatItem } from '@/domains/value/base/floatItem'
import { IntItem } from '@/domains/value/base/intItem'

/**
 * フォーム全体のデータを管理するエンティティ
 */
export class FormEntity {
  constructor(data) {
    this.data = {
      baseModelName: new StringItem(data?.baseModelName),
      baseModelRevision: new StringItem(data?.baseModelRevision),
      compile: new BoolItem(data?.compile),

      loraModelName: new StringItem(data?.loraModelName),
      loraModelRevision: new StringItem(data?.loraModelRevision),
      loraModelWeight: new StringItem(data?.loraModelWeight),

      controlnetModelName: new StringItem(data?.controlnetModelName),
      controlnetModelRevision: new StringItem(data?.controlnetModelRevision),
      controlnetModelWeight: new StringItem(data?.controlnetModelWeight),

      seed: new StringItem(data?.seed),
      generateType: new StringItem(data?.generateType).default('t2i'),

      width: new IntItem(data?.width).default(1024),
      height: new IntItem(data?.height).default(1024),

      strength: new FloatItem(data?.strength).default(0.3),

      prompt: new StringItem(data?.prompt),
      negativePrompt: new StringItem(data?.negativePrompt),

      scheduler: new StringItem(data?.scheduler).default('ddim'),
      inferenceSteps: new IntItem(data?.inferenceSteps).default(30),
      guidanceScale: new FloatItem(data?.guidanceScale).default(8.0),

      memo: new StringItem(data?.memo)
    }
  }

  get hasError() {
    for (const key in this.data) {
      if (this.data[key].hasError) {
        return true
      }
    }
    return false
  }

  getValues() {
    const values = {}
    for (const key in this.data) {
      values[key] = this.data[key].value
    }
    return values
  }
}
