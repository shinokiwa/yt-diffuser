<script setup>
/**
 * メイン表示エリア メニューペイン
 */
import ButtonPrimary from '@/components/form/ButtonPrimary.vue'
import { useEditorStateUseCase } from '@/composables/editorStateUseCase'
const editorState = useEditorStateUseCase()
import { useProjectUseCase } from '@/composables/projectUseCase'
const projectUseCase = useProjectUseCase()
const { project } = projectUseCase.getRefs()

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

    <ButtonPrimary v-if="project.projectName" @click="projectUseCase.close()">
      <i class="bi bi-plus"></i>
      閉じる
    </ButtonPrimary>

    <ButtonPrimary v-if="project.projectName">
      <i class="bi bi-plus"></i>
      追加
    </ButtonPrimary>
  </div>
</template>

<style scoped></style>
