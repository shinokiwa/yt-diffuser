<script setup>
import { ref, onMounted } from 'vue'
import WindowArea from '@/components/elements/WindowArea.vue'
import Overlay from '@/components/elements/Overlay.vue'
import FormGrid from '@/components/elements/FormGrid.vue'
import InputText from '@/components/elements/InputText.vue'

import { useModel } from '@/composables/api/res/model'
const { allModels } = useModel()

import { useGenerateImage } from '@/composables/api/generate/image'
const { loadModel } = useGenerateImage()

import { useApi } from '@/composables/api';
const { get } = useApi()

const addModel = ref(null)

const selectedModel = ref(-1)
const detail = ref(allModels.value[0])

function edit () {
    addModel.value.show()
}

function download () {
    apix.post('/api/worker/download', {})
}

function select (id) {
    selectedModel.value = id
    detail.value = allModels.value.find(model => model.id === id)
}

function load () {
    loadModel(detail.value.model_name, detail.value.revision)
}
</script>

<template>
<WindowArea id="ModelManageView" window-title="モデル一覧">
    <div id="ModelList">
        <ul class="list">
            <li @click="edit()">
                <i class="bi-plus-circle"></i> モデルを新規追加
            </li>
            <li v-for="model in allModels" :key="model.id" @click="select(model.id)">
                <div class="name">{{ model.screen_name || model.model_name }}</div>
                <ul class="info">
                    <li>{{ model.revision }}</li>
                </ul>
            </li>
        </ul>
        <div class="detail">
            <div v-if="selectedModel == -1">
                モデルを選択して下さい。
            </div>
            <div v-else>
                <div class="header">
                    <div class="name">{{ detail.screen_name || detail.model_name }}</div>
                    <div class="menu">
                        <button @click="load">読み込み</button>
                        <ul class="append-menu">
                            <li>編集</li>
                            <li>削除</li>
                        </ul>
                    </div>
                </div>
                <dl>
                    <dt>モデル名</dt>
                    <dd>{{ detail.model_name }}</dd>
                    <dt>リビジョン</dt>
                    <dd>{{ detail.revision }}</dd>
                </dl>
            </div>
        </div>
    </div>
    <Overlay ref="addModel">
        <WindowArea id="AddModelView" window-title="モデル追加" v-bind:close-button="addModel.hide">
            <FormGrid>
                <InputText label="モデルID" placeholder="モデルIDを入力" />
                <InputText label="リビジョン" placeholder="リビジョンを入力" />
            </FormGrid>
            <button @click="download">ダウンロード</button>
            <button>閉じる</button>
        </WindowArea>
    </Overlay>
</WindowArea>
</template>

<style scoped>
#ModelList {
    width: 100%;
    height: 100%;
    border: 1px solid var(--color-border-window);
    border-radius: 4px;
    overflow: hidden;

    display: flex;
    flex-direction: row;
}

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

.detail {
    flex-grow: 1;
    min-height: 100%;
    padding: 10px;
}

.detail .header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    padding-bottom: 5px;
    border-bottom: 1px solid var(--color-border-window);
}

.detail .header > .name {
    font-weight: bold;
}

.detail .header > .menu > .append-menu {
    display: none;
}

button {
    margin: 5px;
    padding: 5px 10px;
    color: var(--font-color-light);
    border: 1px solid var(--color-border-window);
    border-radius: 4px;
    background-color: #33cc44;
    font-weight: bold;
    cursor: pointer;
}

</style>