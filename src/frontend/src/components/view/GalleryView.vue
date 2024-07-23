<script setup>
/**
 * ギャラリービュー
 */
import { ref, onMounted } from 'vue'
import WindowFrame from '@/components/element/WindowFrame.vue'

import { useProjectListUseCase, useProjectUseCase, useAppStateUseCase } from '@/composables/'
import { VIEW_IDS } from '@/types/enum/view'
const projectUseCase = useProjectUseCase()
const listUseCase = useProjectListUseCase()

const gallery = ref([])

onMounted(async () => {
  gallery.value = await listUseCase.fetchAll()
})

async function select(name) {
  await projectUseCase.load(name)
  useAppStateUseCase().changeView(VIEW_IDS.EDITOR)
}
</script>

<template>
  <WindowFrame id="GalleryView" window-title="ギャラリー">
    <div class="gallery-wrapper">
      <div class="gallery-item" v-for="item in gallery" :key="item.name">
        <img v-if="item.thumbnail" :src="item.thumbnail" alt="thumbnail" />
        <a href="#" @click="select(item.name)">{{ item.name }}</a>
      </div>
    </div>
  </WindowFrame>
</template>

<style scoped>
.gallery-item {
  width: 200px;
  height: 200px;
  margin: 10px;
  display: inline-block;
  border: 1px solid #ccc;
  border-radius: 5px;
  overflow: hidden;
}

.gallery-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>
