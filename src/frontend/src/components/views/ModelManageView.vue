<script setup>
import { ref } from 'vue'
import WindowArea from '@/components/elements/WindowArea.vue'
import ModelListArea from '@/components/views/modelmanage/ModelListArea.vue'
import ModelDetailArea from '@/components/views/modelmanage/ModelDetailArea.vue'

const selectedModel = ref("")
</script>

<template>
<WindowArea id="ModelManageView" window-title="モデル一覧">
    <div id="ModelList">
        <ModelListArea v-model="selectedModel" />
        <ModelDetailArea :selected-model="selectedModel" />
    </div>
</WindowArea>
</template>

<style scoped>
#ModelList {
    width: 100%;
    height: 100%;
    border: 1px solid var(--color-border-window);
    border-radius: 4px;
    overflow: hidden;

    display: flex;
    flex-direction: row;
}
</style>