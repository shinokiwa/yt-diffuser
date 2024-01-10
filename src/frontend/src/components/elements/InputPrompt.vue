<script setup>
import {ref, defineProps, defineEmits, watchEffect} from 'vue'
import FormElement from '@/components/elements/FormElement.vue'
    
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
<FormElement :label="label">
    <textarea
        :id="id"
        placeholder="ここに入力"
        v-model="prompt"
    ></textarea>

    <div class="btn-menu">
        <button type="button" title="プロンプトを保存" @click='store.dispatch("image/prompt")'>
            <i class="bi-save2"></i>
        </button>

        <button type="button" title="保存したプロンプトを読み込む" @click='detailEditor=true'>
            <i class="bi-folder-symlink"></i>
        </button>

        <button type="button" title="クリップボードにコピー" @click='copy'>
            <i class="bi-clipboard"></i>
        </button>

        <button type="button" title="プロンプトを全削除" @click='prompt = ""'>
            <i class="bi-trash"></i>
        </button>
    </div>    
</FormElement>
</template>
    
<style scoped>
.form-element {
    padding-bottom: 0;
    padding-left: 0;
    padding-right: 0;
}
textarea {
    height: 8em;
    padding: 0 10px;
    resize: vertical;
    width: 100%;
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

.btn-menu button:hover {
    background-color: var(--color-bg-gray);
}

</style>