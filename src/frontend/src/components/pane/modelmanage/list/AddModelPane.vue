<script setup>
/**
 * モデル新規追加のボタン
 */
import { defineEmits } from 'vue'

defineEmits('click')
</script>

<template>
  <div id="AddModelPane" @click="click"><i class="bi-plus-circle"></i> モデルを新規追加</div>
</template>

<style scoped>
#AddModelPane {
  padding: 10px;
  cursor: pointer;
}

#AddModelPane:hover {
  background-color: var(--color-bg-focus);
}
</style>
