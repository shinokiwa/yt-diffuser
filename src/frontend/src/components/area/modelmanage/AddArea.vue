<script setup>
/**
 * モデル追加表示
 */
import { ref } from 'vue'

import GridArea from '@/components/form/GridArea.vue'
import GridElement from '@/components/form/GridElement.vue'

import { useDownloadUseCase } from '@/composables/download/downloadUseCase'

const modelId = ref('')
const revision = ref('')

function download() {
  const { startDownload } = useDownloadUseCase()
  startDownload(modelId.value, revision.value)
}
</script>

<template>
  <div id="AddModelArea">
    <h3>新規モデルのダウンロード</h3>
    <GridArea>
      <GridElement id="ModelID" label="モデルID">
        <input type="text" placeholder="モデルIDを入力" v-model="modelId" />
      </GridElement>
      <GridElement id="Revision" label="リビジョン">
        <input type="text" placeholder="リビジョンを入力" v-model="revision" />
      </GridElement>

      <GridElement id="ModelType" label="モデル種別">
        <select>
          <option value="1">基本モデル</option>
          <option value="2">LoRA</option>
          <option value="3">ControlNet</option>
        </select>
      </GridElement>
    </GridArea>

    <button @click="download">ダウンロード</button>
  </div>
</template>

<style scoped>
#AddModelArea {
  padding: 10px;
}
</style>
