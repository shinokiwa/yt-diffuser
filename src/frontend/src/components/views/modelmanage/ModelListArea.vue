<script setup>
/**
 * モデルリストエリア
 */
import { ref } from 'vue'

import WindowArea from '@/components/elements/WindowArea.vue'
import InputText from '@/components/elements/InputText.vue'
import Overlay from '@/components/elements/Overlay.vue'
import { useGenerateStatus } from '@/composables/api/generate/status'
const { status, baseModelLabel, loraModelLabel, controlnetModelLabel } = useGenerateStatus()

// v-modelとしてselectedModelを受け取る
const selectedModel = defineModel({ type: String })

import { useModel } from '@/composables/api/res/model'
const { modelList } = useModel()

const addModel = ref(null)
function edit () {
    addModel.value.show()
}

function download () {
    apix.post('/api/worker/download', {})
}

</script>

<template>
<div id="ModelListArea">
    <ul class="list">
        <li id="OpenAddModel" @click="edit()">
            <i class="bi-plus-circle"></i> モデルを新規追加
        </li>
        <li @click="selectedModel = ''">
            <div>
                現在のモデル<br>
                <span v-if="status==='exit' || status===''">なし</span>
                <span v-if="status==='loading'">読み込み中</span>
                <span v-if="status==='ready'">読み込み完了</span>
                <span v-if="status==='generating'">生成中</span>
                <span v-if="status==='error'">エラー</span>
            </div>
            <div class="name">{{ baseModelLabel }}</div>
            <div class="info">
                <div v-if="loraModelLabel !== ''">LoRA : {{ loraModelLabel }}</div>
                <div v-if="controlnetModelLabel !== ''">controlNet : {{ controlnetModelLabel }}</div>
            </div>
        </li>
        <li v-for="model in modelList" :key="model.model_name" @click="selectedModel = model.model_name">
            <div class="name">{{ model.screen_name || model.model_name }}</div>
            <div class="info">
                <span v-if="model.model_class==='base-model'">基本モデル</span>
                <span v-if="model.model_class==='lora-model'">LoRA</span>
                <span v-if="model.model_class==='controlnet-model'">ControlNet</span>
            </div>
        </li>
    </ul>
    <Overlay ref="addModel" id="AddModelOverlay">
        <WindowArea id="AddModelView" window-title="モデル追加" v-bind:close-button="addModel.hide">
            <InputText label="モデルID" placeholder="モデルIDを入力" />
            <InputText label="リビジョン" placeholder="リビジョンを入力" />
            <button @click="download">ダウンロード</button>
            <button>閉じる</button>
        </WindowArea>
    </Overlay>
</div>
</template>

<style scoped>
.list {
    width: 400px;
    height: 100%;
    border-right: 1px solid var(--color-border-window);
    overflow-y: scroll;
}

.list > li {
    padding: 10px;
    border-bottom: 1px solid var(--color-border-window);
    cursor: pointer;
}

.list > li:hover {
    background-color: var(--color-bg-focus);
    color: var(--font-color-light);
}

.list > li > .name {
    font-weight: bold;
}

.list > li > .info {
    font-size: 12px;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}
</style>