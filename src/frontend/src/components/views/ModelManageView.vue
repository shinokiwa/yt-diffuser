<script setup>
import { ref } from 'vue'
import WindowArea from '@/components/elements/WindowArea.vue'
import ListArea from '@/components/views/modelmanage/ListArea.vue'
import CurrentArea from '@/components/views/modelmanage/CurrentArea.vue'
import AddArea from '@/components/views/modelmanage/AddArea.vue'
import DetailArea from '@/components/views/modelmanage/DetailArea.vue'

const viewMode = ref("list")
const selectedModel = ref("")
</script>

<template>
<WindowArea id="ModelManageView" window-title="モデル管理" content-no-padding>
    <div id="ModelManageContent">
        <CurrentArea
            class="pane-current"
        />
        <ListArea
            class="pane-detail"
            v-model:view="viewMode"
            v-model:select="selectedModel"
            v-if="viewMode === 'list'"
        />
        <AddArea
            class="pane-detail"
            v-else-if="viewMode === 'add'"
        />
        <DetailArea
            class="pane-detail"
            v-else-if="viewMode === 'detail'"
            :selected-model="selectedModel"
        />
    </div>
</WindowArea>
</template>

<style scoped>
#ModelManageContent {
    width: 100%;
    height: 100%;
    overflow: hidden;

    display: flex;
    flex-direction: row;
}
.pane-current {
    width: 50%;
    max-width: 400px;
}

.pane-detail {
    flex-grow: 1;
    min-height: 100%;
}

</style>