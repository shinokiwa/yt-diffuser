<script setup>
/**
 * メイン表示エリア レイヤー表示
 */
import { ref, watchEffect } from 'vue'

import MainLayerMenuPane from './MainLayerMenuPane.vue'

import { useProjectLayerUseCase } from '@/composables'
const { getRefs, getImageUrl } = useProjectLayerUseCase()
const { project, isOpen, selectedLayer } = getRefs()

const selectedTab = ref('image')
const source = ref('')

watchEffect(() => {
  if (isOpen.value && selectedLayer.value) {
    source.value = getImageUrl(selectedLayer.value, 'image')
  } else {
    source.value = ''
  }
})
</script>

<template>
  <div id="EditorMainLayer">
    <div v-if="isOpen" class="image-pane">
      <MainLayerMenuPane class="image-menu" />
      <div v-if="source">
        <img :src="source" />
      </div>
      <div v-else>
        レイヤーに画像が設定されていません。<br />
        以下の方法で画像を設定できます。<br />
        ・他の画像をレイヤーに設定する<br />
        ・画像ファイルをアップロードする<br />
        ・クリップボードから貼り付ける
      </div>
    </div>
    <div v-if="isOpen" class="tab-pane">
      <button :class="{ active: selectedTab === 'image' }" @click="selectedTab = 'image'">
        画像
      </button>
      <button :class="{ active: selectedTab === 'i2i' }" @click="selectedTab = 'i2i'">i2i</button>
      <button :class="{ active: selectedTab === 'mask' }" @click="selectedTab = 'mask'">
        マスク
      </button>
      <button :class="{ active: selectedTab === 'cn' }" @click="selectedTab = 'cn'">
        ControlNet
      </button>
    </div>
  </div>
</template>

<style scoped>
#EditorMainLayer {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.image-pane {
  position: relative;
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

.image-menu {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 10;
  height: 40px;
  background-color: rgba(0, 0, 0, 0.5);
  opacity: 0;

  transition: opacity 0.2s ease;
}

.image-pane:hover .image-menu {
  opacity: 1;
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
