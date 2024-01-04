<script setup>
import {ref, defineProps, defineEmits, watchEffect} from 'vue'
    
const props = defineProps({
    id: String,
    label: String,
    promptList: Array,
    modelValue: String
})
const emits = defineEmits(['update:modelValue'])

const prompt = ref(props.modelValue)

watchEffect(()=>{
    emits('update:modelValue', prompt.value)
})

async function copy () {
    try {
        await navigator.clipboard.writeText(prompt.value);
        toast.emit('クリップボードにコピーしました。')
    } catch (err) {
        toast.emit('コピーに失敗しました。')
    }
}
</script>

<template>    
<div class="prompt-area">
    <label :for="id">{{ label }}</label>
    <textarea
        :id="id"
        placeholder="ここに入力"
        v-model="prompt"
    ></textarea>

    <div class="btn-menu">
        <button type="button" title="プロンプトを表示" @click='store.dispatch("image/prompt")'>
            <i class="bi-info-circle"></i>
        </button>

        <button type="button" title="詳細編集" @click='detailEditor=true'>
            <i class="bi-pen"></i>
        </button>

        <button type="button" title="クリップボードにコピー" @click='copy'>
            <i class="bi-clipboard"></i>
        </button>

        <button type="button" title="プロンプトを全削除" @click='prompt = ""'>
            <i class="bi-trash"></i>
        </button>
    </div>    
</div>
</template>
    
    
<style scoped>
.prompt-area {
    position: relative;
    width: 100%;
    margin: 0;
    margin: 11px 0 22px;
    border: 1px solid var(--color-border-window);
    border-radius: 5px;
    background-color: var(--color-bg-base);
    box-sizing: border-box;
}

.prompt-area:has(*:focus) {
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

textarea {
    width: 100%;
    height: 8em;
    font-size: var(--font-size-base);
    margin-top: 10px;
    padding: 10px;
    border: none;
    background-color: transparent;
    box-sizing: border-box;
    resize: vertical;
    border: 0 solid var(--color-border-window);
    border-bottom-width: 1px;
}

textarea::placeholder {
    color: var(--font-color-gray);
}

.btn-menu {
    display: flex;
    flex-direction: row;
    justify-content: end;
    margin-top: -8px;
}
.btn-menu button {
    margin: 0;
    padding: 2px 3px;
    font-size: 18px;
    border-width: 0;
    border-left-width: 1px;
    border-color: var(--color-border-window);
    background-color: var(--color-bg-base);
}

.btn-menu button:disabled:hover {
    background-color: transparent;
}

</style>