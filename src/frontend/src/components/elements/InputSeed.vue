<script setup>
/**
 * SEED値入力フォーム
 * ランダム生成は16桁の整数
 */
import {ref, defineProps, defineEmits, onMounted, watchEffect} from 'vue'
import FormElement from '@/components/elements/FormElement.vue'
    
const props = defineProps({
    id: String,
    label: String,
    modelValue: Number
})
const emits = defineEmits(['update:modelValue'])

const seed = ref(props.modelValue)

function random () {
    seed.value = Math.floor(Math.random() * 10000000000000000)
}

onMounted(()=>{
    if (seed.value === 0) {
        random()
    }
})

watchEffect(()=>{
    emits('update:modelValue', seed.value)
})
</script>

<template>
<FormElement :label="label">
    <button @click="random">ランダム</button>
    <input type="text"
        :id="id"
        placeholder=""
        v-model="seed"
    >
</FormElement>
</template>

<style scoped>
.form-element {
    display: flex;
    flex-direction: row;
}
button {
    margin-right: 10px;
}
input {
    flex-grow: 1;
    border: none;
    background-color: transparent;
    box-sizing: border-box;
    font-size: var(--font-size-base);
    border-width: 0;
}

textarea::placeholder {
    color: var(--font-color-gray);
}
</style>