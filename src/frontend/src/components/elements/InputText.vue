<script setup>
/**
 * テキスト入力フォーム 基本パターン
 * v-model対応
 **/
defineProps({
    id: {
        type: String,
        default: ''
    },
    label: {
        type: String,
        default: ''
    },
    placeholder: {
        type: String,
        default: ''
    },
    modelValue: {
        type: String,
        default: ''
    }
})
defineEmits(['update:modelValue'])
</script>

<template>
<div>
    <label :for="id">{{ label }}</label>
    <input type="text"
        :id="id"
        :placeholder="placeholder"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
    >
</div>

</template>

<style scoped>
div {
    display: flex; flex-direction: row;
}

.grid div {
    display: contents;
}

div > label, div > input {
    margin: 5px 0;
    display: block;
    border-bottom: 1px solid var(--color-border-window);
}
label {
    flex-shrink: 0;
    padding-right: 40px;
}
input {
    border: none;
    flex-grow: 1;
    width: auto;
}
</style>