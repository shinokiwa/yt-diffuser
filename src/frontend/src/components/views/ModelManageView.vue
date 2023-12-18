<script setup>
import { ref } from 'vue'
import WindowArea from '@/components/elements/WindowArea.vue'
import Overlay from '@/components/elements/Overlay.vue'
import FormGrid from '@/components/elements/FormGrid.vue'
import InputText from '@/components/elements/InputText.vue'

import { useApi } from '@/composables/api';

const addModel = ref(null)
const { apix } = useApi()

const models = ref([
    {
        id: 1,
        screen_name: 'StableDiffusion XL',
        name: 'StableDiffusion XL',
        revision: 'main',
        updated_at: '2023-04-02'
    },
    {
        id: 2,
        screen_name: '',
        name: 'StableDiffusion v2.1',
        revision: 'fp16',
        updated_at: '2023-04-02'
    }
])

const selectedModel = ref(null)
const detail = ref(models.value[0])

function edit () {
    addModel.value.show()
}

function download () {
    apix.post('/api/worker/download', {})
}

function select (id) {
    selectedModel.value = id
    detail.value = models.value.find(model => model.id === id)
}
</script>

<template>
<WindowArea id="ModelManageView" window-title="モデル一覧">
    <div id="ModelList">
        <ul class="list">
            <li @click="edit()">
                <i class="bi-plus-circle"></i> モデルを新規追加
            </li>
            <li v-for="model in models" :key="model.id" @click="select(model.id)">
                <div class="name">{{ model.screen_name || model.name }}</div>
                <ul class="info">
                    <li>{{ model.revision }}</li>
                    <li>更新: {{ model.updated_at }}</li>
                </ul>
            </li>
        </ul>
        <div class="detail">
            <div v-if="selectedModel">
                <div class="header">
                    <div class="name">{{ detail.screen_name || detail.name }}</div>
                    <div class="menu">
                        <button>読み込み</button>
                        <ul class="append-menu">
                            <li>編集</li>
                            <li>削除</li>
                        </ul>
                    </div>
                </div>
                <dl>
                    <dt>モデル名</dt>
                    <dd>{{ detail.name }}</dd>
                    <dt>リビジョン</dt>
                    <dd>{{ detail.revision }}</dd>
                    <dt>更新日</dt>
                    <dd>{{ detail.updated_at }}</dd>
                </dl>
            </div>
            <div v-else>
                モデルを選択して下さい。
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