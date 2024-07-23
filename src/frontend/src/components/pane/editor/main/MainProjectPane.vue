<script setup>
/**
 * メイン表示エリア プロジェクト新規作成
 */
import { ref } from 'vue'
import GridArea from '@/components/form/GridArea.vue'
import GridElement from '@/components/form/GridElement.vue'
import ButtonPrimary from '@/components/form/ButtonPrimary.vue'

import { useProjectUseCase } from '@/composables'
const { createProject } = useProjectUseCase()

const projectName = ref('')
const width = ref('')
const height = ref('')

const submit = async () => {
  await createProject(projectName.value, width.value, height.value)
}
</script>

<template>
  <div id="EditorMainProject">
    <GridArea>
      <GridElement label="プロジェクト名">
        <input type="text" v-model="projectName" placeholder="プロジェクト名" />
      </GridElement>
      <GridElement label="幅">
        <input type="text" v-model="width" placeholder="幅" />
      </GridElement>
      <GridElement label="高さ">
        <input type="text" v-model="height" placeholder="高さ" />
      </GridElement>
    </GridArea>
    <ButtonPrimary @click="submit">
      <i class="bi bi-plus"></i>
      プロジェクト新規作成
    </ButtonPrimary>
  </div>
</template>

<style scoped>
#EditorMainimage {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}
</style>
