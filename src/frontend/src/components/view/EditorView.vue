<script setup>
/**
 * 画像編集ビュー
 */
import MainArea from '@/components/area/editor/MainArea.vue'
import PromptArea from '@/components/area/editor/PromptArea.vue'
import LayerArea from '@/components/area/editor/LayerArea.vue'
import ResultArea from '@/components/area/editor/ResultArea.vue'
</script>

<template>
  <div id="EditorView">
    <div class="left">
      <MainArea />
    </div>
    <div class="right">
      <div class="prompt"><PromptArea /></div>
      <div class="layer"><LayerArea /></div>
      <div class="result"><ResultArea /></div>
    </div>
  </div>
</template>

<style scoped>
#EditorView {
  display: flex;
  height: 100%;
}

.left {
  flex: 1;
  height: 100%;
  overflow: auto;
}

.right {
  width: 500px;
  margin-left: 10px;
  height: 100%;
  overflow: auto;

  display: flex;
  flex-direction: column;
}

.prompt {
  margin-bottom: 10px;
  height: 300px;
}

.layer {
  flex: 1;
  margin-bottom: 10px;
}

.result {
  height: 300px;
}
</style>
