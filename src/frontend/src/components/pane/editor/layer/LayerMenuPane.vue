<script setup>
/**
 * レイヤー表示エリア メニューペイン
 */
import ButtonPrimary from '@/components/form/ButtonPrimary.vue'
import { useProjectUseCase, useProjectLayerUseCase, useEditorStateUseCase } from '@/composables/'
const editorState = useEditorStateUseCase()
const projectUseCase = useProjectUseCase()
const layerUseCase = useProjectLayerUseCase()

const { project, isOpen } = projectUseCase.getRefs()
</script>

<template>
  <div id="LayerMenuPane">
    <ButtonPrimary v-if="isOpen" @click="layerUseCase.addLayer('新しいレイヤー')">
      <i class="bi bi-plus"></i>
      追加
    </ButtonPrimary>
  </div>
</template>

<style scoped></style>
