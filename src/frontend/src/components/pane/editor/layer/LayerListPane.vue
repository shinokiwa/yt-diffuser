<script setup>
/**
 * レイヤー表示エリア レイヤーリスト
 */
import LayerItemPane from './LayerItemPane.vue'

import { useProjectUseCase } from '@/composables'
const { getRefs } = useProjectUseCase()

const { project, isOpen } = getRefs()
</script>

<template>
  <div id="LayerListPane">
    <div v-if="isOpen === false">プロジェクトが開かれていません</div>
    <div v-else>
      <div class="list-item" v-for="layerId in project.layers.order" :key="layerId">
        <LayerItemPane :layerId="layerId" />
      </div>
    </div>
  </div>
</template>
