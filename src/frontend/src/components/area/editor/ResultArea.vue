<script setup>
/**
 * 生成結果表示エリア
 */
import { ref } from 'vue'
import WindowFrame from '@/components/element/WindowFrame.vue'
import TempMenuPane from '@/components/pane/editor/result/TempMenuPane.vue'
import TempGalleryPane from '@/components/pane/editor/result/TempGalleryPane.vue'

import ProgressPane from '@/components/pane/editor/result/ProgressPane.vue'
import LogPane from '@/components/pane/editor/result/LogPane.vue'

const selectedTab = ref('gallery')
</script>

<template>
  <WindowFrame id="EditorResultArea">
    <div class="result-area">
      <div id="EditorResultTempPane" v-if="selectedTab === 'gallery'" class="result gallery">
        <TempMenuPane />
        <TempGalleryPane />
      </div>

      <div v-else-if="selectedTab === 'log'" class="result log">
        <LogPane />
      </div>

      <div class="tab-area">
        <button :class="{ active: selectedTab === 'gallery' }" @click="selectedTab = 'gallery'">
          一時保存ギャラリー
        </button>
        <button :class="{ active: selectedTab === 'log' }" @click="selectedTab = 'log'">
          ログ
        </button>
      </div>

      <div class="progress">
        <ProgressPane />
      </div>
    </div>
  </WindowFrame>
</template>

<style scoped>
#EditorResultArea {
  height: 100%;
  overflow: auto;
}

.result-area {
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  height: 100%;
}

.result {
  height: 200px;
  border: 1px solid var(--color-border-window);
  border-bottom-width: 0;
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
  padding: 10px;
}

#EditorResultTempPane {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
}

.tab-area {
  display: flex;
  justify-content: space-around;
  height: 25px;
}

.tab-area button {
  flex-grow: 1;
  background-color: var(--color-bg-back);
  border: 1px solid var(--color-border-window);
  border-bottom-left-radius: 5px;
  border-bottom-right-radius: 5px;
}

.tab-area button.active {
  border-top-width: 0;
  background-color: transparent;
}

.progress {
  margin-top: 5px;
  height: 35px;
}
</style>
