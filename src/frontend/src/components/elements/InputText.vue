<script setup>
/**
 * テキスト入力フォーム 基本パターン
 **/
import FormElement from '@/components/elements/FormElement.vue'
    
const props = defineProps({
    id: {
        type: String,
    },
    label: {
        type: String,
    },
    placeholder: {
        type: String,
        default: ''
    },
})
const modelValue = defineModel({ type: [String, Number], defaultValue: '' })
</script>

<template>
<FormElement :label="label" :id="id">
    <input
        type="text"
        :id="id"
        :placeholder="placeholder"
        v-model="modelValue"
    >
</FormElement>
</template>

<style scoped>
input {
    flex-grow: 1;
    border: none;
    background-color: transparent;
    box-sizing: border-box;
    font-size: var(--font-size-base);
    border: 0 solid var(--color-border-window);
}

input::placeholder {
    color: var(--font-color-gray);
}
</style>