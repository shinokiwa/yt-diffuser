<script setup>
/**
 * フォームのグリッドレイアウト
 * 
 * @prop {string} id - 要素のID
 */
const props = defineProps({
    id: { type: String, default: ''}
}) 
</script>

<template>
<div :id="props.id" class="form-grid">
    <slot></slot>
</div>
</template>

<style scoped>
.form-grid {
    display: grid;
    grid-template-columns: 1fr;
    grid-gap: 5px;
}
</style>