<script setup>
/**
 * フォーム要素外枠
 *
 * @prop {string} id - 要素のID
 * @prop {string} label - フォームのラベル
 */
import { defineProps } from 'vue'
defineProps({
  id: String,
  label: String
})
</script>

<template>
  <div class="grid-form-element">
    <label :for="id">{{ label }}</label>
    <slot />
  </div>
</template>

<style scoped>
.grid-form-element {
  display: grid;
  grid-template-columns: 1fr 2fr; /* ラベルと入力フィールドの幅を指定 */
  gap: 10px; /* ラベルと入力フィールドの間に隙間を設定 */
}
</style>
