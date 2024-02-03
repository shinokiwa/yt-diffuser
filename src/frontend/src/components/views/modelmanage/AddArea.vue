<script setup>
/**
 * モデル追加表示
 */
import { ref } from 'vue'

import InputText from '@/components/elements/InputText.vue'
import InputSelect from '@/components/elements/InputSelect.vue'

function download () {
    apix.post('/api/worker/download', {})
}

</script>

<template>
<div id="AddModelArea">
    <h3>新規モデルのダウンロード</h3>
    <InputText label="モデルID" placeholder="モデルIDを入力" />
    <InputText label="リビジョン" placeholder="リビジョンを入力" />

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