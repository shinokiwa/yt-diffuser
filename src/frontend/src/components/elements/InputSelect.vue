<script setup>
/**
 * 選択フォーム
 **/
import FormElement from '@/components/elements/FormElement.vue'
    
const props = defineProps({
    id: {
        type: String,
    },
    label: {
        type: String,
    },
})
const modelValue = defineModel({ type: [String, Number], defaultValue: '' })
</script>

<template>
<FormElement :label="label" :id="id">
    <select :id="id" v-model="modelValue">
        <slot />
    </select>
</FormElement>
</template>

<style scoped>
select {
    width: 100%;
    border: none;
    background-color: transparent;
    box-sizing: border-box;
    font-size: var(--font-size-base);
    border: 0 solid var(--color-border-window);
}

</style>