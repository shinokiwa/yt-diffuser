<script setup>
/**
 * モデル選択エリア
 */

import { useFormUseCase } from '@/composables/form/formUseCase'
//import { useGenerateProcess } from '@/composables/api/generate/process'
//import { useGenerateStatus } from '@/composables/api/generate/status'

const formUseCase = useFormUseCase()
const { baseModelName, baseModelRevision, compile } = formUseCase.getRefs()
//const { status, baseModelLabel, loraModelLabel, controlnetModelLabel } = useGenerateStatus()

async function load() {
  const { loadModel } = useGenerateProcess()
  await loadModel(baseModelName.value, baseModelRevision.value, compile.value)
  await formUseCase.save()
}

async function remove() {
  const { removeModel } = useGenerateProcess()
  await removeModel()
}

//const { removeLora } = useGenerateProcess()
</script>

<template>
  <div id="LoadModelPane">
    <input type="checkbox" id="IsCompile" v-model="compile" value="1" /><label for="IsCompile"
      >初回生成時にコンパイルする</label
    >
    <div class="menu">
      <button @click="load" :disabled="!baseModelName">読み込み</button>
    </div>
    <ul>
      <li v-if="baseModelLabel !== ''"><button @click="remove">モデルを解放</button> <br /></li>
      <li v-if="loraModelLabel !== ''"><button @click="removeLora">LoRAを解除</button> <br /></li>
    </ul>
  </div>
</template>

<style scoped>
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
