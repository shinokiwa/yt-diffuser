<script setup>
/**
 * ボタンメニュー
 * ほぼスタイル指定のみ
 */
</script>

<template>
<div class="button-menu">
    <slot></slot>
</div>
</template>

<style scoped>
.button-menu {
    display: flex;
    flex-direction: row;
    justify-content: end;
    border: 0 solid var(--color-border-window);
    border-width: 1px 0 1px 0;
}

:slotted(button) {
    margin: 0;
    padding: 2px 3px;
    font-size: 18px;
    border-width: 0;
    border-left-width: 1px;
    border-color: var(--color-border-window);
    background-color: var(--color-bg-base);
}

:slotted(button:hover) {
    background-color: var(--color-bg-gray);
}
</style>