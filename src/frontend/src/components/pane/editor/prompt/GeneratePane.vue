<script setup>
/**
 * 画像編集ビュー プロンプトエリア 生成実行ペイン
 */
import { ref } from 'vue'

// 未整理
import { useFormUseCase } from '@/composables/form/formUseCase'
//import { useGenerateImage } from '@/composables/api/generate/image'

const generateCount = ref(1)

function submit() {
  start(generateCount.value)
}
function start(count) {
  const { start_generate } = useGenerateImage()
  const {
    generateType,
    width,
    height,
    prompt,
    negativePrompt,
    scheduler,
    inferenceSteps,
    guidanceScale,
    strength
  } = useFormUseCase().getRefs()
  start_generate(
    generateType.value,
    count,
    width.value,
    height.value,
    prompt.value,
    negativePrompt.value,
    scheduler.value,
    inferenceSteps.value,
    guidanceScale.value,
    strength.value
  )
}
</script>

<template>
  <div id="EditorPromptGeneratePane">
    <div class="preset">
      <button @click="start(4)">4</button>
      <button @click="start(10)">10</button>
      <button @click="start(20)">20</button>

      <label for="Count">生成枚数</label>
      <input id="Count" type="number" v-model="generateCount" />
      <button id="StartFromCount" @click="submit()">生成</button>
    </div>
  </div>
</template>

<style scoped>
#EditorPromptGeneratePane {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
}

button {
  margin: 5px;
  padding: 5px 10px;
  color: var(--font-color-light);
  border: 1px solid var(--color-border-window);
  border-radius: 4px;
  background-color: #33cc44;
  font-weight: bold;
  cursor: pointer;
}
</style>
