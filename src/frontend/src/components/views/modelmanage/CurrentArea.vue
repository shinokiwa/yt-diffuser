<script setup>
import { ref } from 'vue'

import FormElement from '@/components/elements/FormElement.vue'

import { useGenerateStatus } from '@/composables/api/generate/status'
import { useGenerateProcess } from '@/composables/api/generate/process'
import { useLatestForm } from '@/composables/api/res/form/latest'
import { useFormStore } from '@/composables/store/form'

const { updateLatestForm } = useLatestForm()

const detailMode = defineModel('detail', { type: String })

const {
    baseModelName, baseModelRevision, compile,
    loraModelName, loraModelRevision, loraModelWeight,
    controlnetModelName, controlnetModelRevision, controlnetModelWeight
} = useFormStore()
const { status, baseModelLabel, loraModelLabel, controlnetModelLabel } = useGenerateStatus()

async function load () {
    const { updateLatestForm } = useLatestForm()
    const { loadModel } = useGenerateProcess()
    await loadModel(baseModelName.value, baseModelRevision.value, compile.value)
    await updateLatestForm({baseModelName, baseModelRevision, compile})
}

async function remove () {
    const { removeModel } = useGenerateProcess()
    await removeModel()
}

const { removeLora } = useGenerateProcess()
</script>

<template>
<div id="CurrentModelArea">
    <h3>モデル設定</h3>
    <div>
        <FormElement label="基本モデル">
            {{ baseModelName || '未設定' }}
            <span v-if="baseModelName">{{ baseModelRevision }}</span>
        </FormElement>
        <FormElement label="LoRA">
            {{ loraModelName || '未設定' }}
            <span v-if="loraModelName">{{ controlnetModelRevision }}</span>
        </FormElement>
        <FormElement label="ControlNet">
            {{ controlnetModelName || '未設定' }}
            <span v-if="controlnetModelName">{{ controlnetModelRevision }}</span>
        </FormElement>
        <input type="checkbox" id="IsCompile" v-model="compile" value="1" /><label for="IsCompile">初回生成時にコンパイルする</label>
        <div class="menu">
            <button
                @click="load"
                :disabled="!baseModelName"
            >
                読み込み
            </button>
        </div>
    </div>

    <h3>現在のモデル</h3>
    <div
        v-if="status ==='exit' || status === 'empty' || status === ''"
        class="current-model"
    >
        なし
    </div>
    <div
        v-else
    >
        <div>
            <span v-if="status==='loading'">読み込み中</span>
            <span v-if="status==='ready'">読み込み完了</span>
            <span v-if="status==='compiling'">コンパイル中</span>
            <span v-if="status==='generating'">生成中</span>
            <span v-if="status==='error'">エラー</span>
        </div>
        <div class="name">{{ baseModelLabel }}</div>
        <div class="info">
            <div v-if="loraModelLabel !== ''">LoRA : {{ loraModelLabel }}</div>
            <div v-if="controlnetModelLabel !== ''">controlNet : {{ controlnetModelLabel }}</div>
        </div>
        <ul>
            <li v-if="baseModelLabel !== ''">
                <button @click="remove">モデルを解放</button> <br />
            </li>
            <li v-if="loraModelLabel !== ''">
                <button @click="removeLora">LoRAを解除</button> <br />
            </li>
        </ul>
    </div>

</div>
</template>

<style scoped>
#CurrentModelArea {
    padding: 10px 20px;
    border-right: 1px solid var(--color-border-window);
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