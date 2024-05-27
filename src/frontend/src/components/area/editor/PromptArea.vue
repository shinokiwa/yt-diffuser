<script setup>
/**
 * 画像編集ビュー プロンプトエリア
 */
import { ref } from 'vue'
import WindowFrame from '@/components/element/WindowFrame.vue'

import BasicPane from '@/components/pane/editor/prompt/BasicPane.vue'
import PromptPane from '@/components/pane/editor/prompt/PromptPane.vue'
import NegativePane from '@/components/pane/editor/prompt/NegativePane.vue'
import AdvancedPane from '@/components/pane/editor/prompt/AdvancedPane.vue'

import GeneratePane from '@/components/pane/editor/prompt/GeneratePane.vue'

const selectedTab = ref('basic')
</script>

<template>
  <WindowFrame id="EditorPromptArea">
    <div class="tab-area">
      <button :class="{ active: selectedTab === 'basic' }" @click="selectedTab = 'basic'">
        基本
      </button>
      <button :class="{ active: selectedTab === 'prompt' }" @click="selectedTab = 'prompt'">
        プロンプト
      </button>
      <button :class="{ active: selectedTab === 'negative' }" @click="selectedTab = 'negative'">
        ネガティブ
      </button>
      <button :class="{ active: selectedTab === 'advanced' }" @click="selectedTab = 'advanced'">
        詳細
      </button>
    </div>

    <div v-if="selectedTab === 'basic'" class="input-area">
      <BasicPane />
    </div>

    <div v-else-if="selectedTab === 'prompt'" class="input-area">
      <PromptPane />
    </div>

    <div v-else-if="selectedTab === 'negative'" class="input-area">
      <NegativePane />
    </div>

    <div v-else-if="selectedTab === 'advanced'" class="input-area">
      <AdvancedPane />
    </div>

    <div class="generate-area">
      <GeneratePane />
    </div>
  </WindowFrame>
</template>

<style scoped>
.tab-area {
  display: flex;
  justify-content: space-around;
  height: 25px;
}

.tab-area button {
  flex-grow: 1;
  background-color: var(--color-bg-back);
  border: 1px solid var(--color-border-window);
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
}

.tab-area button.active {
  border-bottom-width: 0;
  background-color: transparent;
}

.input-area {
  height: 200px;
  border: 1px solid var(--color-border-window);
  border-top-width: 0;
  border-bottom-left-radius: 5px;
  border-bottom-right-radius: 5px;
  overflow: hidden;
  padding: 10px;
}

.generate-area {
  display: flex;
  justify-content: center;
  height: 50px;
}
</style>
