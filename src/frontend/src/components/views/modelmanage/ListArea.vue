<script setup>
/**
 * モデルリストエリア
 */
import { useModel } from '@/composables/api/res/model'
import { useFormStore } from '@/composables/store/form'

const viewMode = defineModel('view', { type: String })
const selectedModel = defineModel('select', { type: String })

const { baseModels, loraModels, controlnetModels, lastUsedModel } = useModel()
const { baseModelName, baseModelRevision, loraModelName, loraModelRevision, controlnetModelName, controlnetModelRevision } = useFormStore()

function select (model) {
    baseModelName.value = model.model_name
    baseModelRevision.value = model.revisions[0]
}
</script>

<template>
<div id="ModelListArea">
    <ul class="list">
        <li class="add-model clickable" @click="viewMode = 'add'">
            <i class="bi-plus-circle"></i> モデルを新規追加
        </li>

        <li class="section-title">基本モデル</li>
        <li
            v-for="model in baseModels"
            :key="model.model_name"
            class="model-item clickable"
        >
            <div
                class="model"
                @click="select(model)"
            >
                {{ model.screen_name || model.model_name }}
            </div>
            <div
                class="info"
            >
                <i class="bi-info-circle"></i>
            </div>
        </li>
        <li class="section-title">LoRA</li>
        <li class="section-title">ControlNet</li>
    </ul>
</div>
</template>

<style scoped>
.list {
    height: 100%;
    overflow-y: scroll;
}

.list > li {
    border-bottom: 1px solid var(--color-border-window);
}

.list > li.add-model {
    padding: 10px;
    background-color: var(--color-bg-weight);
    font-weight: bold;
}

.list > li.section-title {
    padding: 5px;
    font-weight: bold;
    color: var(--font-color-light);
    background-color: var(--color-bg-sectionheader);
}

.list > li.model-item {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    padding: 10px;
}

.list > li.clickable {
    cursor: pointer;
}

.list > li.clickable:hover {
    background-color: var(--color-bg-focus);
}

.list > li.model-item > .model {
    font-weight: bold;
    flex-grow: 1;
}

.list > li.model-item > .info {
    font-size: 18px;
    width: 40px;
    text-align: center;
}

.list > li.model-item > .info:hover {
    color: var(--font-color-blue);
}
</style>