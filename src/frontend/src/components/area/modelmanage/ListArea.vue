<script setup>
/**
 * モデルリストエリア
 */
import { onMounted } from 'vue'
import { useModelUseCase } from '@/composables/model/modelUseCase'
const modelUseCase = useModelUseCase()

const viewMode = defineModel('viewMode', { type: String })
const selectedModel = defineModel('selectedModel', { type: String })

const { baseModels, loraModels, controlnetModels } = modelUseCase.getRefs()

// 表示時にモデル一覧を取得
onMounted(async () => {
  await modelUseCase.fetchAll()
})

function selectModel(model) {
  viewMode.value = 'detail'
  selectedModel.value = model.modelName
}
</script>

<template>
  <div id="ModelListArea">
    <ul class="list">
      <li class="add-model clickable" @click="viewMode = 'add'">
        <i class="bi-plus-circle"></i> モデルを新規追加
      </li>

      <li class="current-model clickable" @click="viewMode = 'current'">現在のモデル</li>

      <li class="section-title">基本モデル</li>
      <li
        v-for="model in baseModels"
        :key="model.modelName"
        class="model-item clickable"
        @click="selectModel(model)"
      >
        {{ model.screenName || model.modelName }}
      </li>
      <li class="section-title">LoRA</li>
      <li class="section-title">ControlNet</li>
    </ul>
  </div>
</template>

<style scoped>
.list {
  height: 100%;
  overflow-y: scroll;
}

.list > li {
  border-bottom: 1px solid var(--color-border-window);
}

.list > li.add-model {
  padding: 10px;
  background-color: var(--color-bg-weight);
  font-weight: bold;
}

.list > li.section-title {
  padding: 5px;
  font-weight: bold;
  color: var(--font-color-light);
  background-color: var(--color-bg-sectionheader);
}

.list > li.model-item,
.list > li.current-model {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  padding: 10px;
}

.list > li.clickable {
  cursor: pointer;
}

.list > li.clickable:hover {
  background-color: var(--color-bg-focus);
}

.list > li.model-item > .model {
  font-weight: bold;
  flex-grow: 1;
}

.list > li.model-item > .info {
  font-size: 18px;
  width: 40px;
  text-align: center;
}

.list > li.model-item > .info:hover {
  color: var(--font-color-blue);
}
</style>
