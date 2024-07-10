<script setup>
/**
 * レイヤー表示エリア レイヤーリスト
 */
import ImageThumb from '@/components/element/ImageThumb.vue'

import { useEditorStateUseCase } from '@/composables/editorStateUseCase'
const { changeMainToLayer } = useEditorStateUseCase()
import { useProjectUseCase } from '@/composables/projectUseCase'
const projectUseCase = useProjectUseCase()
const { project, isOpen } = projectUseCase.getRefs()

function selectLayer(layerId) {
  projectUseCase.selectLayer(layerId)
  changeMainToLayer()
}
</script>

<template>
  <div id="LayerListPane">
    <div v-if="isOpen === false">プロジェクトが開かれていません</div>
    <div v-else class="list-item" v-for="layerId in project.layers.order" :key="layerId">
      <div class="layer-thumb" @click="selectLayer(layerId)">
        <ImageThumb
          :src="
            'output/project/' +
            project.projectName +
            '/layers/' +
            layerId +
            '/' +
            project.layers.layers[layerId].image
          "
          :cacheBuster="true"
        />
      </div>
      <div class="layer-info">
        {{ project.layers.layers[layerId].layerName }}
      </div>
    </div>
  </div>
</template>

<style scoped>
.list-item {
  padding: 5px;
  border-bottom: 1px solid var(--color-border-window);
  display: flex;
  align-items: center;
  flex-direction: row;
}
.list-item:hover {
  background-color: var(--color-bg-focus);
}
.layer-thumb {
  width: 50px;
  height: 50px;
}
.layer-info {
  margin-left: 5px;
  display: flex;
  align-items: center;
  flex-direction: column;
}
</style>
