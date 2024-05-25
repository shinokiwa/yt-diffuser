<script setup>
/**
 * ギャラリービュー
 */
import { ref, onMounted, onUnmounted } from 'vue'
import WindowArea from '@/components/elements/WindowArea.vue'
import Overlay from '@/components/elements/Overlay.vue'
import FormGrid from '@/components/elements/FormGrid.vue'
import InputText from '@/components/elements/InputText.vue'

import { useImage } from '@/composables/api/res/image'
const { getImageList } = useImage()

const imageList = ref([])
let source = null

onMounted(()=>{
    source = getImageList('images', (data)=>{
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
<WindowArea id="GalleryView" window-title="ギャラリー">
    <div class="gallery">
        <div class="gallery-item" v-for="image in imageList" :key="image.id">
            <img :src="'output/images/' + image.url">
        </div>
    </div>
</WindowArea>
</template>

<style scoped>
.gallery-item {
    width: 200px;
    height: 200px;
    margin: 10px;
    display: inline-block;
    border: 1px solid #ccc;
    border-radius: 5px;
    overflow: hidden;
}

.gallery-item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
</style>