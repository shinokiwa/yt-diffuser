<script setup>
/**
 * 画像ビューアー
 */
import { ref, watch } from 'vue'
import Overlay from '@/components/elements/Overlay.vue'

import { useViewerStore } from '@/composables/store/viewer'
const {
    showViewer,
    hideViewer,

    isShowViewer,
    imageUrl,
    nextCallback,
    prevCallback,
    deleteCallback
} = useViewerStore()

const viewer = ref(null)
</script>

<template>
<div id="ImageView">
    <Overlay
        ref="viewer"
        v-model:isShow="isShowViewer"
    >
        <div class="viewer">
            <img :src="imageUrl" />
        </div>
    </Overlay>
</div>
</template>

<style scoped>
.viewer img {
    display: block;
    padding: 20px;
    max-height: 100vh;
    object-fit: contain;
}
</style>