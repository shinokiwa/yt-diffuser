<script setup>
/**
 * 選択モデル表示エリア
 */
import { useFormUseCase } from '@/composables/form/formUseCase'
const {
  baseModelName,
  baseModelRevision,
  loraModelName,
  controlnetModelName,
  controlnetModelRevision
} = useFormUseCase().getRefs()
</script>

<template>
  <div id="CurrentModelArea">
    <h3>モデル設定</h3>
    <div class="form-element">
      <label>基本モデル</label>
      {{ baseModelName || '未設定' }}
      <span v-if="baseModelName">{{ baseModelRevision }}</span>
    </div>

    <div class="form-element">
      <label>LoRA</label>
      {{ loraModelName || '未設定' }}
      <span v-if="loraModelName">{{ controlnetModelRevision }}</span>
    </div>

    <div class="form-element">
      <label>ControlNet</label>
      {{ controlnetModelName || '未設定' }}
      <span v-if="controlnetModelName">{{ controlnetModelRevision }}</span>
    </div>
  </div>
</template>

<style scoped>
/** スタイルは前バージョンのを流用しているだけなので後でなんとかしたい。 */
.form-element {
  position: relative;
  width: 100%;
  margin: 11px 0 22px;
  padding: 16px 10px 10px;
  border: 1px solid var(--color-border-window);
  border-radius: 5px;
  background-color: var(--color-bg-base);
  box-sizing: border-box;
}

.form-element:has(*:focus) {
  box-shadow: 0 0 2px 3px var(--color-shadow);
}

label {
  position: absolute;
  display: block;
  top: -11px;
  left: 10px;
  z-index: 1;
  color: var(--font-color-gray);
  background-color: var(--color-bg-base);
  width: auto !important;
}
</style>
