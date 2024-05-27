<script setup>
/**
 * メイン表示エリア
 */
import { ref } from 'vue'
import WindowFrame from '@/components/element/WindowFrame.vue'

import { useEditorStateUseCase } from '@/composables/app/editorStateUseCase'
const { mainImage } = useEditorStateUseCase().getRefs()

const image = ref(null)
</script>

<template>
  <WindowFrame id="EditorMainArea">
    <img id="EditorMainImage" ref="image" :src="mainImage" />
  </WindowFrame>
</template>

<style scoped>
#EditorMainArea {
  height: 100%;
}

#EditorMainImage {
  width: 100%;
  height: calc(100% - 20px);
  object-fit: contain;
}
</style>
