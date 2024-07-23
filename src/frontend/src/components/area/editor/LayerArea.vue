<script setup>
/**
 * メイン表示エリア
 */
import WindowFrame from '@/components/element/WindowFrame.vue'
import LayerMenuPane from '@/components/pane/editor/layer/LayerMenuPane.vue'
import LayerListPane from '@/components/pane/editor/layer/LayerListPane.vue'
</script>

<template>
  <WindowFrame id="EditorLayerArea">
    <div class="layer-area">
      <div class="title">レイヤー</div>
      <div class="list">
        <LayerListPane />
      </div>
      <div class="menu">
        <LayerMenuPane />
      </div>
    </div>
  </WindowFrame>
</template>

<style scoped>
#EditorLayerArea {
  height: 100%;
}

.layer-area {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.menu {
  height: 50px;
}
.list {
  flex-grow: 1;
  border: 1px solid var(--color-border-window);
  overflow-y: scroll;
}
</style>
