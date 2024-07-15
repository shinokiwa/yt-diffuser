<script setup>
/**
 * レイヤー表示エリア メニューペイン
 */
import ButtonPrimary from '@/components/form/ButtonPrimary.vue'
import { useProjectEditUseCase, useProjectListUseCase, useEditorStateUseCase } from '@/composables/'
const editorState = useEditorStateUseCase()
const projectEdit = useProjectEditUseCase()
const projectList = useProjectListUseCase()

const { project } = projectEdit.getRefs()

function createProject() {
  editorState.changeMainToProject()
}
</script>

<template>
  <div id="LayerMenuPane">
    <ButtonPrimary v-if="project.projectName === ''" @click="createProject">
      <i class="bi bi-plus"></i>
      プロジェクト新規作成
    </ButtonPrimary>

    <ButtonPrimary v-if="project.projectName" @click="projectList.close()">
      <i class="bi bi-plus"></i>
      閉じる
    </ButtonPrimary>

    <ButtonPrimary v-if="project.projectName" @click="projectEdit.addLayer('新しいレイヤー')">
      <i class="bi bi-plus"></i>
      追加
    </ButtonPrimary>
  </div>
</template>

<style scoped></style>
