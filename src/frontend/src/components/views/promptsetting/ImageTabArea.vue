<script setup>
import { ref } from 'vue'
import PreviewArea from '@/components/views/promptsetting/PreviewArea.vue'
import InputImageArea from '@/components/views/promptsetting/InputImageArea.vue'

import { useOutputPreview } from '@/composables/api/res/output/preview'
const { previewSrc } = useOutputPreview()

const mode = ref('preview')

</script>

<template>
<div class="image-tab-area">
    <div class="menu">
        <button :class="{active: mode === 'preview'}" @click="mode = 'preview'">プレビュー</button>
        <button :class="{active: mode === 'source'}" @click="mode = 'source'">ソース</button>
        <button :class="{active: mode === 'mask'}" @click="mode = 'mask'">マスク</button>
        <button :class="{active: mode === 'control'}" @click="mode = 'control'">ControlNet</button>
    </div>
    <PreviewArea
        v-if="mode === 'preview'"
        class="input-image-area"
        :src="previewSrc"
    />
    <InputImageArea
        v-if="mode === 'source'"
        class="input-image-area"
        src="/input/source.png"
        image-type="source"
    />

    <InputImageArea
        v-if="mode === 'mask'"
        class="input-image-area"
        src="/input/mask.png"
        image-type="mask"
    />


    <InputImageArea
        v-if="mode === 'control'"
        class="input-image-area"
        src="/input/controlnet.png"
        image-type="controlnet"
    />
</div>
</template>

<style scoped>
.image-tab-area .menu {
    display: flex;
    justify-content: space-around;
}

.image-tab-area .menu button {
    flex-grow: 1;
    background-color: var(--color-bg-back);
    border: 1px solid var(--color-border-window);
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
}

.image-tab-area .menu button.active {
    border-bottom-width: 0;
    background-color: transparent;
}

.image-tab-area .input-image-area {
    width: 400px;
    height: 400px;
    border: 1px solid var(--color-border-window);
    border-top-width: 0;
    border-bottom-left-radius: 5px;
    border-bottom-right-radius: 5px;
    overflow: hidden;
}

</style>