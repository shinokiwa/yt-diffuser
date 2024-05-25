<script setup>
/**
 * 画像のサムネイル表示
 * 遅延読み込みに対応
 */
import { onMounted, onUnmounted, defineProps, ref } from 'vue'
import { useImageObserver } from '@/composables/store/imageobserver';

const props = defineProps({
    src: String
})

const image = ref(null)

onMounted(() => {
    const { observer } = useImageObserver()
    observer.observe(image.value)
})
onUnmounted(() => {
    const { observer } = useImageObserver()

    if (image.value) {
        observer.unobserve(image.value)
    }
})
</script>

<template>
    <img ref="image" :data-src="props.src" />
</template>
  
