<script setup>
/**
 * モデル管理ビュー
 */
import { ref } from 'vue'

import WindowFrame from '@/components/element/WindowFrame.vue'
import ListArea from '@/components/area/modelmanage/ListArea.vue'
import AddArea from '@/components/area/modelmanage/AddArea.vue'
import CurrentArea from '@/components/area/modelmanage/CurrentArea.vue'
import DetailArea from '@/components/area/modelmanage/DetailArea.vue'

const viewMode = ref('list')
const selectedModel = ref('')
</script>

<template>
  <WindowFrame window-title="モデル管理" content-no-padding>
    <div id="ModelManageView">
      <div class="list-area">
        <ListArea v-model:view="viewMode" v-model:select="selectedModel" />
      </div>
      <div class="detail-area">
        <AddArea v-if="viewMode === 'add'" />
        <CurrentArea v-else-if="viewMode === 'current'" />
        <DetailArea v-else-if="viewMode === 'detail'" :selected-model="selectedModel" />
      </div>
    </div>
  </WindowFrame>
</template>

<style scoped>
#ModelManageView {
  width: 100%;
  height: 100%;
  overflow: hidden;

  display: flex;
  flex-direction: row;
}
</style>
