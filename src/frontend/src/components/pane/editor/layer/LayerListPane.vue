<script setup>
/**
 * レイヤー表示エリア レイヤーリスト
 */
import LayerItemPane from './LayerItemPane.vue'

import { useProjectEditUseCase } from '@/composables'
const { getRefs } = useProjectEditUseCase()

const { project, isOpen } = getRefs()
</script>

<template>
  <div id="LayerListPane">
    <div v-if="isOpen === false">プロジェクトが開かれていません</div>
    <div v-else>
      <div class="list-item">
        <!--<LayerItemPane layerId="" />-->
      </div>
      <div class="list-item" v-for="layerId in project.layers.order" :key="layerId">
        <LayerItemPane
          :projectName="project.projectName"
          :layerId="layerId"
          :layer="project.layers.layers[layerId]"
        />
      </div>
    </div>
  </div>
</template>
