<script setup>
/**
 * 第１優先ボタンの共通コンポーネント
 */
const emits = defineEmits(['click'])
</script>

<template>
  <button class="button-primary" @click="emits('click')">
    <slot></slot>
  </button>
</template>

<style scoped>
button {
  margin: 5px;
  padding: 5px 10px;
  color: var(--font-color-light);
  border: 1px solid var(--color-border-window);
  border-radius: 4px;
  background-color: #3910ec;
  font-weight: bold;
  cursor: pointer;
}
</style>
