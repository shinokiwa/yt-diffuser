<script setup>
/**
 * 画像編集ビュー プロンプトエリア プロンプトペイン
 */
import { onUnmounted } from 'vue'
import InputPrompt from '@/components/form/InputPrompt.vue'

import { useFormUseCase } from '@/composables/form/formUseCase'
const formUseCase = useFormUseCase()
const { prompt } = formUseCase.getRefs()

onUnmounted(() => {
  formUseCase.save()
})
</script>

<template>
  <div class="pane-prompt">
    <InputPrompt id="prompt" v-model="prompt"></InputPrompt>
  </div>
</template>

<style scoped>
.pane-prompt {
  height: 100%;
  width: 100%;
}
</style>
