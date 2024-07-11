<script setup>
/**
 * メイン表示エリア
 */
import { ref, watchEffect } from 'vue'

import { useProjectEditUseCase } from '@/composables'
const { getRefs, getImageUrl } = useProjectEditUseCase()
const { project, isOpen, selectedLayer } = getRefs()

const selectedTab = ref('image')
const source = ref('')

watchEffect(() => {
  if (isOpen.value && selectedLayer.value) {
    source.value = getImageUrl(
      project.value.projectName,
      selectedLayer.value,
      project.value.layers.layers[selectedLayer.value].image
    )
  } else {
    source.value = ''
  }
})
</script>

<template>
  <div id="EditorMainLayer">
    <div v-if="isOpen" class="image-pane">
      <img :src="source" />
    </div>
    <div v-if="isOpen" class="tab-pane">
      <button :class="{ active: selectedTab === 'image' }" @click="selectedTab = 'image'">
        画像
      </button>
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
