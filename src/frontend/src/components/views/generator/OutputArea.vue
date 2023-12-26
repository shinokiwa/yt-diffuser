<script setup>
/**
 * 生成ビューの出力エリア
 */
import { ref, onMounted, onUnmounted } from 'vue'
import WindowArea from '@/components/elements/WindowArea.vue'

import { useTemp } from '@/composables/api/res/output/temp'
const { imageList, refresh, close, deleteAll, deleteSelected } = useTemp()

onMounted(()=>{
    refresh()
})

onUnmounted(()=>{
    close()
})

const isSelected = ref(false)

function toggleSelect (id) {
    let selected = false
    imageList.value.forEach(image => {
        if (image.id === id) {
            image.selected = !image.selected
        }

        if (image.selected) {
            selected = true
        }
    })
    isSelected.value = selected
}
</script>

<template>
<WindowArea window-title="出力画像">
    <div class="menu">
        <button @click="refresh">更新</button>
        <button v-if="isSelected" @click="deleteSelected">選択したものを削除</button>
        <button @click="deleteAll">すべて削除</button>
    </div>
    <div class="gallery">
        <a
            class="gallery-item"
            v-for="image in imageList"
            :key="image.id"
            :class="{ selected: image.selected }"
            href="#"
            @click="toggleSelect(image.id)"
        >
            <img
                :src="'output/temp/' + image.url + '?t=' + image.timestamp"
            >
        </a>
    </div>
</WindowArea>
</template>

<style scoped>

.menu {
    display: flex;
    justify-content: flex-end;
}

.menu button {
    margin: 5px;
}
.gallery {
    display: flex;
    flex-wrap: wrap;
    justify-content: flex-start;
    word-wrap: break-word;
}

.gallery-item {
    width: 150px;
    height: 150px;
    margin: 5px;
    padding: 5px;
    display: inline-block;
    box-sizing: content-box;
}

.gallery-item:hover {
    cursor: pointer;
}

.gallery-item:focus {
    outline: 1px solid #333333;
    background-color: #3344cc;
}

.gallery-item.selected {
    background-color: #3344cc;
}

.gallery-item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
</style>