<script setup>
import { ref } from 'vue'
import FormElement from '@/components/elements/FormElement.vue'
import Overlay from '@/components/elements/Overlay.vue'
import WindowArea from '@/components/elements/WindowArea.vue'
import ButtonMenu from '@/components/elements/ButtonMenu.vue'

const props = defineProps({
    id: String,
    label: String,
    load: Function,
    trash: Function,
})
const prompt = defineModel()

const events = defineEmits(['save'])

const promptList = ref([])
const savedArea = ref(null)

async function copy () {
    try {
        await navigator.clipboard.writeText(prompt.value);
        toast.emit('クリップボードにコピーしました。')
    } catch (err) {
        toast.emit('コピーに失敗しました。')
    }
}

async function showSavedArea () {
    if (props.load === undefined) {
        return
    }
    const data = await props.load()
    promptList.value = data
    savedArea.value.show()
}

function selectPrompt (value) {
    prompt.value = value
    savedArea.value.hide()
}

async function trash (id) {
    if (props.trash === undefined) {
        return
    }
    await props.trash(id)
    promptList.value = promptList.value.filter(item => item.id !== id)
}

</script>

<template>
<FormElement :label="label">
    <textarea
        :id="id"
        placeholder="ここに入力"
        v-model="prompt"
    ></textarea>

    <ButtonMenu class="button-menu">
        <button type="button" title="プロンプトを保存" @click="events('save', prompt)">
            <i class="bi-save2"></i>
        </button>

        <button type="button" title="保存したプロンプトを読み込む" @click='showSavedArea'>
            <i class="bi-folder-symlink"></i>
        </button>

        <button type="button" title="クリップボードにコピー" @click='copy'>
            <i class="bi-clipboard"></i>
        </button>

        <button type="button" title="プロンプトを全削除" @click='prompt = ""'>
            <i class="bi-trash"></i>
        </button>
    </ButtonMenu>
    <Overlay ref="savedArea">
        <WindowArea window-title="保存したプロンプト" v-bind:close-button="savedArea.hide">
            <ul class="saved-list">
                <li v-for="item in promptList" :key="item.id">
                    <div class="trash-button" @click="trash(item.id)">
                        <i class="bi-trash"></i>
                    </div>
                    <div class="prompt" @click="selectPrompt(item.prompt)">
                        {{ item.prompt }}
                    </div>
                </li>
            </ul>
        </WindowArea>
    </Overlay>
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

.button-menu {
    margin-top: -9px;
    border-bottom-width: 0;
    border-radius: 0 0 5px 5px;
    overflow: hidden;
}

.saved-list {
    margin: 10px;
    border-top: 1px solid var(--color-border-window);
}

.saved-list > li {
    padding: 5px;
    border-bottom: 1px solid var(--color-border-window);
    cursor: pointer;

    display: flex;
    flex-direction: row-reverse;
}

.saved-list > li > div:hover {
    background-color: var(--color-bg-focus);
    color: var(--font-color-light);
}

.saved-list > li > .trash-button {
    margin-left: 10px;
    width: 40px;

    display: flex;
    align-items: center;
    justify-content: center;
}

.saved-list > li > .prompt {
    flex-grow: 1;
    flex-shrink: 1;
    width: 100%;
    word-wrap: break-word;
    word-break: break-all;
}


</style>