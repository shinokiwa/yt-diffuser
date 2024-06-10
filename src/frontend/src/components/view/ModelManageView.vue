<script setup>
/**
 * モデル管理ビュー
 */
import { ref } from 'vue'

import WindowFrame from '@/components/element/WindowFrame.vue'
import ListArea from '@/components/area/modelmanage/ListArea.vue'
import AddArea from '@/components/area/modelmanage/AddArea.vue'
import DetailArea from '@/components/area/modelmanage/DetailArea.vue'

import { useModelUseCase } from '@/composables/model/modelUseCase'
import { useFormUseCase } from '@/composables/form/formUseCase'

const { getRefs } = useFormUseCase()
const { baseModelName } = getRefs()

const { findModelByName } = useModelUseCase()
const selectedModel = ref(findModelByName(baseModelName))

const viewMode = ref('add')
if (selectedModel.value) {
  viewMode.value = 'detail'
}
</script>

<template>
  <WindowFrame window-title="モデル管理" content-no-padding>
    <div id="ModelManageView">
      <div class="list-area">
        <ListArea v-model:viewMode="viewMode" v-model:selectedModel="selectedModel" />
      </div>
      <div class="detail-area">
        <AddArea v-if="viewMode === 'add'" />
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

.list-area {
  max-width: 400px;
  height: 100%;
  overflow-y: auto;
}

.detail-area {
  flex-grow: 1;
  height: 100%;
  overflow-y: auto;
}
</style>
