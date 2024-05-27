<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  selectedModel: {
    type: String,
    default: ''
  }
})
/*
import { useModel } from '@/composables/api/res/model'
const { baseModels } = useModel()

import { useGenerateProcess } from '@/composables/api/generate/process'

const selectedRevision = ref('main')

const detail = ref({})

watch(props, () => {
  detail.value = baseModels.value.find((model) => model.model_name === props.selectedModel)
})

const modelName = ref('')
const screenName = ref('')

function load() {
  const { loadModel } = useGenerateProcess()
  loadModel(props.selectedModel, selectedRevision.value)
}

const { removeModel, removeLora } = useGenerateProcess()
*/
</script>

<template>
  <div id="ModelDetailArea">
    <div class="header">
      <div class="name">{{ detail.screen_name || detail.model_name }}</div>
      <div class="menu">
        <button @click="load">読み込み</button>
      </div>
    </div>
    <div>
      <label for="modelName">表示名</label>
      <input
        type="text"
        id="modelName"
        placeholder="一覧に表示する名称を入力"
        v-model="screenName"
      />
    </div>
    <dl>
      <dt>モデル名</dt>
      <dd>{{ detail.model_name }}</dd>
      <dt>モデル種別</dt>
      <dd v-if="detail.model_class === 'base-model'">基本モデル</dd>
      <dd v-if="detail.model_class === 'lora-model'">LoRA</dd>
      <dd v-if="detail.model_class === 'controlnet-model'">ControlNet</dd>
      <dt>リビジョン</dt>
      <dd v-for="(revision, index) in detail.revisions" :key="index">{{ revision }}</dd>
    </dl>
    <div>
      <ul class="append-menu">
        <li>編集</li>
        <li>削除</li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
#ModelDetailArea {
  flex-grow: 1;
  min-height: 100%;
  padding: 10px;
}

#ModelDetailArea .header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  padding-bottom: 5px;
  border-bottom: 1px solid var(--color-border-window);
}

#ModelDetailArea .header > .name {
  font-weight: bold;
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
