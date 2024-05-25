<script setup>
/**
 * モデル追加表示
 */
import { ref } from 'vue'

import InputText from '@/components/elements/InputText.vue'
import InputSelect from '@/components/elements/InputSelect.vue'

import { useDownload } from '@/composables/api/download/index'

const modelId = ref('')
const revision = ref('')

function download () {
    const { startDownload } = useDownload()
    startDownload(modelId.value, revision.value)
}

</script>

<template>
<div id="AddModelArea">
    <h3>新規モデルのダウンロード</h3>
    <InputText label="モデルID" placeholder="モデルIDを入力" v-model="modelId" />
    <InputText label="リビジョン" placeholder="リビジョンを入力" v-model="revision" />

    <InputSelect label="モデル種別">
        <option value="1">基本モデル</option>
        <option value="2">LoRA</option>
        <option value="3">ControlNet</option>
    </InputSelect>
    <button @click="download">ダウンロード</button>
</div>
</template>

<style scoped>
#AddModelArea {
    padding: 10px;
}

</style>