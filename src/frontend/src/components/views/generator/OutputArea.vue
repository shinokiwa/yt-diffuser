<script setup>
/**
 * 生成ビューの出力エリア
 */
import { ref, onMounted, onUnmounted } from 'vue'
import WindowArea from '@/components/elements/WindowArea.vue'

import { useImage } from '@/composables/api/res/image'
const { getImageList } = useImage()

const imageList = ref([])
let source = null

onMounted(()=>{
    source = getImageList('temp', (data)=>{
        if (data.type === 'deleted' || data.type === 'modified') {
            imageList.value = imageList.value.filter((item) => {
                return item.url !== data.target
            })
        }

        if (data.type === 'created' || data.type === 'list' || data.type === 'modified') {
            imageList.value.push({
                id: imageList.value.length,
                url: data.target
            })
        }
    })
})

onUnmounted(()=>{
    source.close()
})
</script>

<template>
<WindowArea window-title="出力画像">
    <div class="gallery">
        <div class="gallery-item" v-for="image in imageList" :key="image.id">
            <img :src="'output/temp/' + image.url">
        </div>
    </div>
</WindowArea>
</template>

<style scoped>
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
    display: inline-block;
}

.gallery-item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
</style>