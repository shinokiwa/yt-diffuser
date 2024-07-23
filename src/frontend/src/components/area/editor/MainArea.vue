<script setup>
/**
 * メイン表示エリア
 */
import WindowFrame from '@/components/element/WindowFrame.vue'
import MainLayerPane from '@/components/pane/editor/main/MainLayerPane.vue'
import MainPreviewPane from '@/components/pane/editor/main/MainPreviewPane.vue'
import MainProjectPane from '@/components/pane/editor/main/MainProjectPane.vue'

import { useEditorStateUseCase, useProjectUseCase } from '@/composables'
const projectUseCase = useProjectUseCase()
const editorState = useEditorStateUseCase()

const { project, isOpen } = projectUseCase.getRefs()
const { mainArea } = editorState.getRefs()

function createProject() {
  editorState.changeMainToProject()
}
</script>

<template>
  <WindowFrame id="EditorMainArea">
    <div class="main">
      <div class="project-info" v-if="isOpen === false">
        <span>プロジェクトが開かれていません</span>
        <button @click="createProject">
          <i class="bi bi-plus"></i>
          プロジェクト新規作成
        </button>
      </div>
      <div class="project-info" v-else>
        <span>プロジェクト名: {{ project.projectName }} </span>
        <button @click="projectUseCase.close()">
          <i class="bi bi-plus"></i>
          プロジェクトを閉じる
        </button>
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
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
.main-area {
  flex-grow: 1;
  max-height: calc(100% - 30px);
}
</style>
