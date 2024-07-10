<script setup>
/**
 * エディタービュー 生成結果表示エリア 一時保存ギャラリー メニュー部品
 */
import { useTempImageUseCase } from '@/composables'
const tempImage = useTempImageUseCase()

const { deleteAll } = {}

function clickDeleteAll() {
  if (window.confirm('全ての画像を削除しますか？')) {
    deleteAll()
  }
}

async function reload() {
  await tempImage.update()
}

async function deleteImage() {
  tempImage.deleteImage()
}
</script>

<template>
  <div id="EditorResultTempMenuPane">
    <button @click="reload" title="リロード">
      <i class="bi-arrow-clockwise"></i>
    </button>
    <button @click="deleteImage">
      <i class="bi-eraser-fill"></i>
    </button>
    <button @click="clickDeleteAll" title="全て削除">
      <i class="bi-trash"></i>
    </button>
  </div>
</template>

<style scoped>
#EditorResultTempMenuPane {
  height: 30px;
  display: flex;
  justify-content: flex-end;
  padding: 5px;
}

button {
  background-color: #aaaaaa;
  margin-left: 5px;
}

button:hover {
  background-color: #3344aa;
}
</style>
