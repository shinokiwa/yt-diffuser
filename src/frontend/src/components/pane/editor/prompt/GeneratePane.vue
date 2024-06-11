<script setup>
/**
 * 画像編集ビュー プロンプトエリア 生成実行ペイン
 */
import { ref } from 'vue'

import { useGenerateUseCase } from '@/composables/generate/generateUseCase'

const generateCount = ref(1)

function submit() {
  start(generateCount.value)
}
async function start(count) {
  const { text_to_image } = useGenerateUseCase()
  await text_to_image(count)
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
