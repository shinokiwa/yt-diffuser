<script setup>
/**
 * モデルリストエリア
 */
import AddModelPane from '@/components/pane/modelmanage/list/AddModelPane.vue'
import ModelListPane from '@/components/pane/modelmanage/list/ModelListPane.vue'

const viewMode = defineModel('viewMode', { type: String })
const selectedModel = defineModel('selectedModel', { type: String })
</script>

<template>
  <div id="ModelListArea">
    <div class="add-model">
      <AddModelPane @click="viewMode = 'add'" />
    </div>
    <div class="model-list">
      <ModelListPane
        :base-models="baseModels"
        :lora-models="loraModels"
        :controlnet-models="controlnetModels"
        v-model:viewMode="viewMode"
        v-model:selected-model="selectedModel"
      />
    </div>
  </div>
</template>

<style scoped>
#ModelListArea {
  height: 100%;
  overflow-y: scroll;
}

.add-model {
  margin: 15px 0;
}
</style>
