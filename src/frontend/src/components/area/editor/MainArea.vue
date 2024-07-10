<script setup>
/**
 * メイン表示エリア
 */
import WindowFrame from '@/components/element/WindowFrame.vue'
import MainLayerPane from '@/components/pane/editor/main/MainLayerPane.vue'
import MainPreviewPane from '@/components/pane/editor/main/MainPreviewPane.vue'
import MainProjectPane from '@/components/pane/editor/main/MainProjectPane.vue'

import { useEditorStateUseCase, useProjectUseCase } from '@/composables'
const editorState = useEditorStateUseCase()
const { project, isOpen } = useProjectUseCase().getRefs()

const { mainArea } = editorState.getRefs()
</script>

<template>
  <WindowFrame id="EditorMainArea">
    <div class="main">
      <div class="project-info">
        <div v-if="isOpen === false">プロジェクトが開かれていません</div>
        <div v-else>プロジェクト名: {{ project.projectName }}</div>
      </div>
      <div class="main-area">
        <MainLayerPane v-if="mainArea === 'layer'" />
        <MainPreviewPane v-else-if="mainArea === 'preview'" />
        <MainProjectPane v-else-if="mainArea === 'project-new'" />
      </div>
    </div>
  </WindowFrame>
</template>

<style scoped>
#EditorMainArea {
  height: 100%;
}
.main {
  height: 100%;
  display: flex;
  flex-direction: column;
}
.project-info {
  height: 30px;
  padding: 5px;
}
.main-area {
  flex-grow: 1;
}
</style>
