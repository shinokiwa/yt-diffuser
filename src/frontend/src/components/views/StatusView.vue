<script setup>
/**
 * フッター部ステータス表示エリア
 */
import { ref } from 'vue'
import { useStatus } from '@/composables/api/sse/status'
const { status } = useStatus()


const progress = ref('10 / 100 (10%) 10s')
</script>

<template>
<div class="status-wrapper">
    <div class="status">{{ status }}</div>
    <div class="progress">{{ progress }}</div>

</div>
</template>

<style scoped>
.status-wrapper {
    box-sizing: content-box;
    background-color: var(--color-bg-header);
    color: var(--font-color-gray);
    border-top: 1px solid var(--color-border-dark);

    display: flex; flex-direction: row; justify-content: start;
}

.status-wrapper div {
    padding: 1px 10px;
}

.status {
    width: 150px;
    background-color: #33ff88;
    text-align: center;
    color: var(--font-color-base);
}
</style>