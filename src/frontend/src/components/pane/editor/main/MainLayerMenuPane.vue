<script setup>
/**
 * メイン表示エリア レイヤー表示 メニュー
 */
import { ref } from 'vue'

import { useProjectLayerUseCase } from '@/composables'
const { uploadImage } = useProjectLayerUseCase()

/**
 * ファイル選択フォーム
 * @type {HTMLInputElement}
 */
const inputfile = ref(null)

/**
 * ファイル選択フォームを開いてアップロード
 */
function upload() {
  inputfile.value.click()

  inputfile.value.addEventListener('change', () => {
    const file = inputfile.value.files[0]
    uploadImage('image', file)
  })
}
</script>

<template>
  <div class="image-menu">
    <button title="ファイルを選択" @click="upload"><i class="bi-files"></i>アップロード</button>
    <button title="削除" class="end" @click="upload"><i class="bi-trash"></i>画像を削除</button>
    <input type="file" ref="inputfile" class="hidden" @change="upload" />
  </div>
</template>

<style scoped>
.image-menu {
  display: flex;
  justify-content: flex-start;
  padding: 4px;
}
button {
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 2px;
  margin: 4px;
}
button.end {
  margin-left: auto;
}
.hidden {
  display: none;
}
</style>
