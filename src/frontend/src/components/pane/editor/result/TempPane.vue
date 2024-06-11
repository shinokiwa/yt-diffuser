<script setup>
/**
 * エディタービュー 生成結果表示エリア 一時保存ギャラリー
 */
import { onMounted, onUnmounted, ref } from 'vue'

import ImageThumb from '@/components/element/ImageThumb.vue'

import { useTempImageUseCase } from '@/composables/tempimage/tempImageUseCase'
import { useEditorStateUseCase } from '@/composables/app/editorStateUseCase'
const tempImage = useTempImageUseCase()
const editor = useEditorStateUseCase()

const imageList = tempImage.getImageList()

//import { useTemp } from '@/composables/api/res/output/temp'
//const { imageList, refresh, close, deleteAll } = useTemp()
const { close, deleteAll } = {}

const galleryItem = ref(null)

onMounted(async () => {
  await tempImage.update()
})

onUnmounted(() => {
  //close()
})

function selectImage(src) {
  editor.changeMainImage(src)
}

function clickDeleteAll() {
  if (window.confirm('全ての画像を削除しますか？')) {
    deleteAll()
  }
}

const reloadSwitch = ref(false)
async function reload() {
  await tempImage.update()
  reloadSwitch.value = !reloadSwitch.value
}
</script>

<template>
  <div id="EditorResultTempPane">
    <div class="button-area">
      <button @click="reload" title="リロード">
        <i class="bi-arrow-clockwise"></i>
      </button>
      <button>
        <i class="bi-eraser-fill"></i>
      </button>
      <button @click="clickDeleteAll" title="全て削除">
        <i class="bi-trash"></i>
      </button>
    </div>

    <div class="gallery-wrapper">
      <div class="gallery" :key="reloadSwitch">
        <div
          class="gallery-item"
          v-for="(image, index) in imageList"
          :key="index"
          ref="galleryItem"
        >
          <ImageThumb :src="'output/temp/' + image" :cacheBuster="true" @click="selectImage" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
#EditorResultTempPane {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
}

.button-area {
  height: 30px;
  display: flex;
  justify-content: flex-end;
  padding: 5px;
}

.button-area button {
  background-color: #aaaaaa;
  margin-left: 5px;
}

.button-area button:hover {
  background-color: #3344aa;
}

.gallery-wrapper {
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
  margin-right: 5px;
}
</style>
