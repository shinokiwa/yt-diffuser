<script setup>
/**
 * プライマリボタン
 */
defineEmits(['click'])
</script>

<template>
  <button class="button-primary" @click="$emit('click')">
    <slot></slot>
  </button>
</template>

<style scoped>
button {
  margin: 5px;
  padding: 5px 10px;
  border: 1px solid var(--color-border-window);
  border-radius: 4px;
  color: var(--font-color-light);
  background-color: var(--color-bg-accent);
  font-weight: bold;
  cursor: pointer;
}
</style>
