<script setup>
import { ref } from 'vue'
import WindowArea from '@/components/elements/WindowArea.vue'
import Overlay from '@/components/elements/Overlay.vue'
import FormGrid from '@/components/elements/FormGrid.vue'
import InputText from '@/components/elements/InputText.vue'

import { useApi } from '@/composables/api';

import { useGlobals } from '@/composables/global';
const { currentView } = useGlobals()

const addModel = ref(null)

function edit () {
    addModel.value.show()
}

const { api } = useApi()

function download () {
    api.post('/api/worker/download', {})
}

</script>

<template>
<WindowArea id="ModelManageView" window-title="モデル一覧">
    <div id="ModelList">
        <div class="model-card new-model" @click="edit()">
            <span class="add-button">
                <i class="bi-plus"></i>
            </span>
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
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: left;
}
.model-card {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 250px;
    height: 400px;
    border: 1px solid var(--color-border-window);
    border-radius: 4px;
    margin: 10px;
}

.model-card.new-model {
    cursor: pointer;
}

.model-card .add-button {
    text-align: center;
    font-size: 100px;
    color: var(--color-border-window);
}
</style>