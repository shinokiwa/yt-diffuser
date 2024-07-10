<script setup>
/**
 * エディタービュー 生成結果表示エリア 一時保存ギャラリー 画像部分
 */
import { ref, onMounted } from 'vue'

import ImageThumb from '@/components/element/ImageThumb.vue'

import { useTempImageUseCase, useEditorStateUseCase } from '@/composables'
const tempImage = useTempImageUseCase()
const editor = useEditorStateUseCase()

const { imageList } = tempImage.getRefs()
const galleryItem = ref(null)

tempImage.useStream()

onMounted(async () => {
  await tempImage.update()
})

function selectImage(image) {
  tempImage.selectImage(image)
  editor.changeMainToPreview()
}
</script>

<template>
  <div id="EditorResultTempGalleryPane">
    <div class="gallery">
      <div
        class="gallery-item"
        v-for="image in imageList"
        :key="image.uuid"
        ref="galleryItem"
        :class="{ selected: image.selected }"
      >
        <ImageThumb
          :uuid="image.uuid"
          :src="image.path + image.name"
          :cacheBuster="true"
          @click="selectImage(image)"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
#EditorResultTempGalleryPane {
  flex: 1;
  width: 100%;
  overflow-x: scroll;
  overflow-y: hidden;
}

.gallery {
  display: flex;
  width: auto;
  flex-wrap: nowrap;
}

.gallery-item {
  display: inline-block;
  flex: 0 0 auto;
  height: 100px;
  width: 100px;
  padding: 2px;
  margin-right: 5px;
}

.gallery-item.selected {
  border: 2px solid var(--color-border-selected);
  padding: 0;
}
</style>
