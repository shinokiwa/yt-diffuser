<script setup>
/**
 * フォームのグリッドレイアウト
 */
</script>

<template>
<div class="grid">
    <slot></slot>
</div>
</template>

<style scoped>
.grid {
    display: grid;
    grid-template-columns: max-content 1fr;
    grid-gap: 0;
}
</style>