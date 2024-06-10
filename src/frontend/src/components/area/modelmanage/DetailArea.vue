<script setup>
import { ref, watch } from 'vue'
import ButtonPrimary from '@/components/form/ButtonPrimary.vue'

import { useModelUseCase } from '@/composables/model/modelUseCase'

const props = defineProps({
  selectedModel: {
    type: String,
    default: ''
  }
})

const { findModelByName, loadModel } = useModelUseCase()
const model = ref(findModelByName(props.selectedModel))

const screenName = ref(model.value.screenName)

watch(props, () => {
  model.value = findModelByName(props.selectedModel)
})

async function load() {
  await loadModel(model.value.modelName, model.value.revisions[0], false)
}
</script>

<template>
  <div id="ModelDetailArea">
    <h3>{{ model.screenName || model.modelName }}</h3>
    <nav>
      <ButtonPrimary @click="load">読み込み</ButtonPrimary>
    </nav>
    <div class="detail-grid">
      <div class="grid-label">表示名</div>
      <div class="grid-desc">
        <input
          type="text"
          id="modelName"
          placeholder="一覧に表示する名称を入力"
          v-model="screenName"
        />
      </div>

      <div class="grid-label">モデル名</div>
      <div class="grid-desc">{{ model.modelName }}</div>

      <div class="grid-label">モデル種別</div>
      <div class="gird-desc">
        <span v-if="model.modelClass === 'base-model'">基本モデル</span>
        <span v-else-if="model.modelClass === 'lora-model'">LoRA</span>
        <span v-else-if="model.modelClass === 'controlnet-model'">ControlNet</span>
      </div>

      <div class="grid-label">リビジョン</div>
      <div class="gird-desc">
        <ul>
          <li v-for="(revision, index) in model.revisions" :key="index">{{ revision }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
#ModelDetailArea {
  padding: 10px;
}

h3 {
  font-size: 2em;
  padding-bottom: 5px;
  border-bottom: 1px solid var(--color-border-window);
}

nav {
  padding: 5px;
  border-bottom: 1px solid var(--color-border-window);
}

.detail-grid {
  margin-top: 20px;
  display: grid;
  grid-template-columns: max-content auto;
  column-gap: 20px;
}

.grid-label {
  font-weight: bold;
}

.grid-desc {
  display: flex;
  align-items: center;
}
</style>
