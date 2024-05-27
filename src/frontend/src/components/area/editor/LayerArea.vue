<script setup>
/**
 * メイン表示エリア
 */
import { ref, onMounted, onUnmounted } from 'vue'
import WindowFrame from '@/components/element/WindowFrame.vue'
</script>

<template>
  <WindowFrame id="GalleryView" window-title="プロンプト">
    <div class="gallery"></div>
  </WindowFrame>
</template>
