<script setup>
/**
 * フォーム要素外枠
 */
import { defineProps } from 'vue'
const props = defineProps({
    id: String,
    label: String,
})
</script>

<template>    
<div class="form-element">
    <label :for="id">{{ label }}</label>
    <slot />
</div>
</template>

<style scoped>
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