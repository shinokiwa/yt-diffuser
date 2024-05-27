<script setup>
/**
 * ギャラリービュー
 */
//import { ref, onMounted, onUnmounted } from 'vue'
import WindowFrame from '@/components/element/WindowFrame.vue'
</script>

<template>
  <WindowFrame id="GalleryView" window-title="ギャラリー">
    <div class="gallery"></div>
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
