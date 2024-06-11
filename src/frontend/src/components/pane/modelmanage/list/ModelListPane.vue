<script setup>
/**
 * モデル一覧のペイン
 */
import { onMounted } from 'vue'

import { useModelUseCase } from '@/composables/model/modelUseCase'
const modelUseCase = useModelUseCase()

const { baseModels, loraModels, controlnetModels } = modelUseCase.getRefs()

const selectedModel = defineModel('selectedModel', { type: String })
const viewMode = defineModel('viewMode', { type: String })

// 表示時にモデル一覧を更新
onMounted(async () => {
  await modelUseCase.fetchAll()
})

function selectModel(model) {
  viewMode.value = 'detail'
  selectedModel.value = model.id
}
</script>

<template>
  <div id="ModelListPane">
    <h3>基本モデル</h3>
    <ul>
      <li
        v-for="model in baseModels"
        :key="model.id"
        class="model-item clickable"
        :class="{ 'selected-model': model.id === selectedModel }"
        @click="selectModel(model)"
      >
        <div class="model-name">
          {{ model.screenName || model.id }}
        </div>
        <div class="last-used">
          <i class="bi-star"></i>
        </div>
      </li>
    </ul>
    <h3>LoRA</h3>
    <h3>ControlNet</h3>
  </div>
</template>

<style scoped>
h3 {
  font-weight: bold;
  border-bottom: 1px solid var(--color-border-window);
  color: var(--font-color-light);
  background-color: var(--color-bg-sectionheader);
  padding: 5px;
}

li {
  border-bottom: 1px solid var(--color-border-window);
  padding: 10px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  cursor: pointer;
}

li.selected-model {
  background-color: var(--color-bg-weight);
}

li:hover {
  background-color: var(--color-bg-focus);
}

li .model {
  font-weight: bold;
  flex-grow: 1;
}

li .info {
  font-size: 18px;
  width: 40px;
  text-align: center;
}
</style>
