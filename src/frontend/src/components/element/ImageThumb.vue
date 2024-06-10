<script setup>
/**
 * 画像のサムネイル表示
 * 遅延読み込みに対応していて、要素がウィンドウに表示された時に読み込みを開始する
 */
import { defineProps, ref } from 'vue'

import { useImageObserver } from '@/composables/app/imageobserver'

const props = defineProps({
  src: String,
  cacheBuster: {
    type: Boolean,
    default: false
  }
})
defineEmits(['click'])

const image = ref(null)
useImageObserver(image)
</script>

<template>
  <img
    ref="image"
    :data-src="props.src"
    :data-cache-buster="props.cacheBuster ? Date.now() : null"
    @click="$emit('click', props.src)"
  />
</template>

<style scoped>
img {
  width: 100%;
  height: auto;
}
</style>
