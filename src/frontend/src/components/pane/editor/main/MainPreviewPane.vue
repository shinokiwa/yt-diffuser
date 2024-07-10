<script setup>
/**
 * メイン表示エリア
 */
import { ref, watchEffect } from 'vue'

import { useTempImageUseCase } from '@/composables'
const { imageList, selectedIndex } = useTempImageUseCase().getRefs()

const selectedTab = ref('image')
const mainImage = ref('')

watchEffect(() => {
  if (selectedIndex.value === -1) {
    mainImage.value = ''
  } else {
    const image = imageList.value[selectedIndex.value]
    mainImage.value = image ? image.path + image.name : ''
  }
})
</script>

<template>
  <div id="EditorMainPreview">
    <div class="image-pane">
      <img :src="mainImage" />
    </div>
    <div class="tab-pane">
      <button :class="{ active: selectedTab === 'image' }" @click="selectedTab = 'image'">
        画像
      </button>
      <button :class="{ active: selectedTab === 'prompt' }" @click="selectedTab = 'prompt'">
        プロンプト表示
      </button>
    </div>
  </div>
</template>

<style scoped>
#EditorMainPreview {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.image-pane {
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  max-height: calc(100% - 25px);
  padding: 5px;
  border: 1px solid var(--color-border-window);
  border-bottom-width: 0;
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
}

.tab-pane {
  display: flex;
  justify-content: space-around;
  height: 25px;
}

.tab-pane button {
  flex-grow: 1;
  background-color: var(--color-bg-back);
  border: 1px solid var(--color-border-window);
  border-bottom-left-radius: 5px;
  border-bottom-right-radius: 5px;
}

.tab-pane button.active {
  border-top-width: 0;
  background-color: transparent;
}

img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}
</style>
