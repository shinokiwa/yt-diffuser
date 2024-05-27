<script setup>
/**
 * モデル管理ビュー モデル読み込みエリア
 */
import SelectedModelPane from '@/components/pane/modelmanage/loadmodel/SelectedModelPane.vue'
import LoadModelPane from '@/components/pane/modelmanage/loadmodel/LoadModelPane.vue'
import CurrentModelPane from '@/components/pane/modelmanage/loadmodel/CurrentModelPane.vue'
</script>

<template>
  <div id="LoadModelArea">
    <SelectedModelPane />
    <LoadModelPane />
    <CurrentModelPane />
  </div>
</template>

<style scoped>
#LoadModelArea {
  padding: 10px 20px;
  border-right: 1px solid var(--color-border-window);
}
</style>
