<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import WindowArea from '@/components/elements/WindowArea.vue'
import GalleryArea from '@/components/elements/GalleryArea.vue'

import { useTemp } from '@/composables/api/res/output/temp'
const { imageList, refresh, close, deleteAll, deleteSelected } = useTemp()

onMounted(()=>{
    refresh()
})

onUnmounted(()=>{
    close()
})

const gallery = ref(null)

const is_enable_delete = ref(false)

function doDeleteSelected (selectItems) {
    deleteSelected(selectItems)
    is_enable_delete.value = false
}

function selected (selectCount) {
    is_enable_delete.value = selectCount > 0
}

function doDeleteAll () {
    window.confirm('すべて削除しますか？') && deleteAll()
}
</script>

<template>
<WindowArea window-title="一時保存ギャラリー" activate="1">
    <div class="temp-gallery">
        <div class="menu">
            <button @click="refresh">更新</button>
            <button v-if="is_enable_delete" @click="gallery.deleteSelected">選択したものを削除</button>
            <button @click="doDeleteAll">すべて削除</button>
        </div>
        <GalleryArea
            class="temp-gallery-area"
            :fileList="imageList"
            ref="gallery"
            baseDir="output/temp/"
            @delete="doDeleteSelected"
            @select="is_enable_delete = true"
            @clear="is_enable_delete = false"
        />
    </div>
</WindowArea>
</template>

<style scoped>
.temp-gallery {
    display: flex;
    flex-direction: column;
}

.menu {
    display: flex;
    justify-content: flex-end;
}

.menu button {
    margin: 5px;
}

.temp-gallery-area {
    flex-grow: 1;
}
</style>