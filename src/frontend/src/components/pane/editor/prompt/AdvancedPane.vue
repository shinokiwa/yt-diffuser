<script setup>
/**
 * 画像編集ビュー プロンプトエリア 詳細設定ペイン
 */
import { onUnmounted } from 'vue'

import GridArea from '@/components/form/GridArea.vue'
import GridElement from '@/components/form/GridElement.vue'

import { useFormUseCase } from '@/composables/form/formUseCase'
const formUseCase = useFormUseCase()
const { scheduler, inferenceSteps, guidanceScale } = formUseCase.getRefs()

onUnmounted(() => {
  formUseCase.save()
})
</script>

<template>
  <GridArea>
    <GridElement id="Scheduler" label="スケジューラー">
      <select v-model="scheduler">
        <option value="ddim">DDIM</option>
        <option value="pndm">PNDM</option>
        <option value="deis">DEIS Multi</option>
        <option value="dpms-singlestep">DPM-Solver++ (Singlestep)</option>
        <option value="dpms-multistep">DPM-Solver++ (Multistep)</option>
        <option value="euler">Euler Discrete</option>
        <option value="euler-ancestral">Euler Ancestral</option>
        <option value="lcm">LCM</option>
      </select>
    </GridElement>

    <GridElement id="Steps" label="ステップ数">
      <input type="number" v-model="inferenceSteps" />
    </GridElement>

    <GridElement id="GuidanceScale" label="ガイダンススケール">
      <input type="number" v-model="guidanceScale" />
    </GridElement>
  </GridArea>
</template>
