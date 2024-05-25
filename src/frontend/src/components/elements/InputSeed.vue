<script setup>
/**
 * SEED値入力フォーム
 * ランダム生成は16桁の整数
 */
import {ref, onMounted, watchEffect} from 'vue'
import FormElement from '@/components/elements/FormElement.vue'
    
const props = defineProps({
    id: {
        type: String,
        default: ''
    },
    label: {
        type: String,
        default: ''
    }
})
const seed = defineModel({ type: Number, defaultValue: 0 })

function random () {
    seed.value = Math.floor(Math.random() * 10000000000000000)
}

onMounted(()=>{
    if (seed.value === 0) {
        random()
    }
})
</script>

<template>
<FormElement :id="id" :label="label">
    <button @click="random">ランダム</button>
    <input type="text"
        :id="id"
        v-model="seed"
    >
</FormElement>
</template>

<style scoped>
.form-element {
    display: flex;
    flex-direction: row-reverse;
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
    border: 0 solid var(--color-border-window);
    border-bottom-width: 1px;
}

textarea::placeholder {
    color: var(--font-color-gray);
}
</style>