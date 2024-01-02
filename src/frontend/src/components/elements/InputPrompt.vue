<script setup>
import {ref, defineProps, defineEmits, watchEffect} from 'vue'
    
const props = defineProps({
    id: String,
    modelValue: Array,
    label: String
})
const emits = defineEmits(['update:modelValue'])

const text = ref(props.modelValue[0])

watchEffect(()=>{
    emits('update:modelValue', text.value)
})

async function copy () {
    try {
        await navigator.clipboard.writeText(text.value);
        toast.emit('クリップボードにコピーしました。')
    } catch (err) {
        toast.emit('コピーに失敗しました。')
    }
}
</script>

<template>    
<div>
    <label :for="id">{{ label }}</label>
    <textarea
        :id="id"
        placeholder="プロンプトを入力"
        v-model="text"
    ></textarea>

    <div class="btn-menu textarea-menu">
        <button type="button" title="プロンプトを表示" @click='store.dispatch("image/prompt")'>
            <i class="bi-info-circle"></i>
        </button>

        <button type="button" title="詳細編集" @click='detailEditor=true'>
            <i class="bi-pen"></i>
        </button>

        <button type="button" title="クリップボードにコピー" @click='copy'>
            <i class="bi-clipboard"></i>
        </button>

        <button type="button" title="プロンプトを全削除" @click='text = ""'>
            <i class="bi-trash"></i>
        </button>
    </div>    
</div>
</template>
    
    
<style scoped>
textarea {
    width: 100%;
    font-size: var(--font-size-base);
    margin: 0; padding: 10px;
    border: 1px solid var(--color-border-window);
    background-color: var(--color-background);
    box-sizing: border-box;
    resize: vertical;
}

textarea::placeholder {
    color: var(--color-mid1)
}

.title {
    position: absolute;
    top: -11px;
    z-index: 1;
    color: var(--color-mid2);
    background-color: var(--color-background);
    width: auto !important;
}

.btn-menu {
    display: flex;
    flex-direction: row;
    justify-content: end;
}
.btn-menu button {
    font-size: 18px;
    border-left-width: 0;
}
.btn-menu button:first-of-type {
    border-left-width: 1px;
}

.btn-menu button:disabled:hover {
    background-color: transparent;
}


/**
 * フォーム関連
 */
.form-area {
    position: relative;
    border: none;
    border-radius: 5px;
    padding: 0;
    -webkit-transition: box-shadow .2s ease-in-out;
    transition: box-shadow .2s ease-in-out;
    width: 100%;
}

.form-area:has(*:focus) {
    box-shadow: 0 0 2px 5px var(--color-shadow);
}

.form-area .title {
    margin-left: 10px;
 }

.form-area input,
.form-area select {
    border-radius: 5px;
}

.form-area textarea {
    border-radius: 5px 5px 0 0;
}

.btn-menu.textarea-menu {
    width: 100%;
    margin: -5px 0 0 0;
    border: 1px solid var(--color-mid2);
    border-radius: 0 0 5px 5px;
    box-sizing: border-box;
}
.btn-menu.textarea-menu button {
    border-top-width: 0;
    border-bottom-width: 0;
    box-sizing: border-box;
}
.btn-menu.textarea-menu button:last-of-type {
    border-bottom-right-radius: 5px;
    border-right-width: 0;
}


/**
 * ユーティリティ
 */
.flex {
    display: flex;
    flex-direction: row;
    gap: 20px;
}
.flex div {
    width: 100%;
}

.border {
    border: 1px solid var(--color-mid2);
    border-radius: 5px;
}

.hidden {
    display: none;
}

.text-info {
    color: #3208eb;
}

.mb-1 {
    margin-bottom: 5px !important;
}

.mb-2 {
    margin-bottom: 10px !important;
}

.mb-3 {
    margin-bottom: 15px !important;
}

.mb-4 {
    margin-bottom: 20px !important;
}
</style>