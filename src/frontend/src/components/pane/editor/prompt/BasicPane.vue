<script setup>
/**
 * 画像編集ビュー プロンプトエリア 基本設定ペイン
 */
import { onUnmounted } from 'vue'

import GridArea from '@/components/form/GridArea.vue'
import GridElement from '@/components/form/GridElement.vue'

import { useFormUseCase } from '@/composables/form/formUseCase'
const formUseCase = useFormUseCase()
const { generateType, seed, height, width, strength } = formUseCase.getRefs()

onUnmounted(() => {
  formUseCase.save()
})
</script>

<template>
  <GridArea>
    <GridElement id="Process" label="生成方法">
      <select v-model="generateType">
        <option value="t2i">Text to Image</option>
        <option value="i2i">Image to Image</option>
        <option value="inpaint">InPaint</option>
      </select>
    </GridElement>

    <GridElement id="Strength" label="強度" v-if="generateType !== 't2i'">
      <input type="number" v-model="strength" />
    </GridElement>

    <GridElement id="Width" label="幅(px)" v-if="generateType === 't2i'">
      <input type="number" v-model="width" />
    </GridElement>

    <GridElement id="Height" label="高さ(px)" v-if="generateType === 't2i'">
      <input type="number" v-model="height" />
    </GridElement>

    <InputSeed id="Seed" label="SEED値" v-model="seed" />
  </GridArea>
</template>
