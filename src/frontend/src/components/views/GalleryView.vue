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
const source = ref(null)

onMounted(()=>{
    source.value = getImageList('', (data)=>{
        console.log (data)
        imageList.value.push({
            id: imageList.value.length,
            url: "data/output/images/" + data
        })
    })
})

onUnmounted(()=>{
    source.value.close()
})

</script>

<template>
<WindowArea id="GalleryView" window-title="ギャラリー">
    <div class="gallery">
        <div class="gallery-item" v-for="image in imageList" :key="image.id">
            <img :src="image.url">
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