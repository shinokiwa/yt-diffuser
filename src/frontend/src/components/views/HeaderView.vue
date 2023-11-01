<script setup>
/**
 * ヘッダーのコンポーネント
 */

import { useStatus } from '@/composables/api/sse/status'
const { status } = useStatus()

</script>

<template>
<header>
    <h1><i class="bi-cpu"></i>&nbsp;ゆとりでふーざー</h1>
    <div>{{ status }}</div>
</header>
</template>

<style scoped>
header {
    background-color: var(--color-bg-header);
    padding: 4px 5px;
    color: var(--font-color-light);
    display: flex; flex-direction: row; justify-content: space-between;
}

header h1 {
    font-size: 14px;
}
</style>