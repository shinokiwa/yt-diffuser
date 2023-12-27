<script setup>
/**
 * 生成ビューの出力エリア
 */
import { ref, onMounted, onUnmounted, watch} from 'vue'
import WindowArea from '@/components/elements/WindowArea.vue'

import { useTemp } from '@/composables/api/res/output/temp'
const { imageList, refresh, close, deleteAll, deleteSelected } = useTemp()

onMounted(()=>{
    refresh()
})

onUnmounted(()=>{
    close()
})

const selectImgs = ref([])
const lastSelectIndex = ref(null)

function selectItem (event, index, image) {
    event.preventDefault()
    event.stopPropagation()
    // Ctrlキーが押されていない場合は選択状態を解除
    if (!event.ctrlKey) {
        selectImgs.value = []
    }

    // Shiftキーが押されている場合は範囲選択
    if (event.shiftKey && lastSelectIndex.value !== null) {
        const range = [lastSelectIndex.value, index].sort()
        imageList.value.forEach((v, i) => {
            if (i >= range[0] && i <= range[1]) {
                selectImgs.value.push(v.url)
            }
        })
    } else {
        if (selectImgs.value.includes(image.url)) {
            selectImgs.value = selectImgs.value.filter(url => url !== image.url)
        } else {
            selectImgs.value.push(image.url)
        }
        lastSelectIndex.value = index
    }

    return false
}

function clearSelect () {
    selectImgs.value = []
    lastSelectIndex.value = null
}


function keyDown (event) {
    if (event.key === 'ArrowRight') {
        const nextItem = event.target.nextElementSibling
        if (nextItem) {
            nextItem.focus()
            nextItem.click()
        }
    } else if (event.key === 'ArrowLeft') {
        const prevItem = event.target.previousElementSibling
        if (prevItem) {
            prevItem.focus()
            prevItem.click()
        }
    }
}

</script>

<template>
<WindowArea window-title="出力画像">
    <div class="menu">
        <button @click="refresh">更新</button>
        <button v-if="selectImgs.length > 0" @click="deleteSelected">選択したものを削除</button>
        <button @click="deleteAll">すべて削除</button>
    </div>
    <div class="gallery"
        @click="clearSelect"
    >
        <a
            class="gallery-item"
            v-for="(image, index) in imageList"
            :key="image.id"
            :class="{ selected: selectImgs.includes(image.url) }"
            :href="'output/temp/' + image.url + '?t=' + image.timestamp"
            target="_blank"

            @click="selectItem($event, index, image)"
            @keydown="keyDown"
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
    outline: 0;
    box-shadow: 0 0 0 2px #333333;
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