<script setup>
/**
 * エディタービュー 生成結果表示エリア 進捗表示
 */
import ProgressBar from '@/components/element/ProgressBar.vue'
//import { useGenerateProgress } from '@/composables/api/generate/progress'

const {
  generateTotal,
  generateCount,

  percentage,
  elapsed,
  remaining,
  average
} = { elapsed: 1.0, remaining: 1.0, average: 1.0 } /* = useGenerateProgress()*/
</script>

<template>
  <div id="EditorResultProgressPane">
    <div class="progress-bar"><ProgressBar :value="percentage" /></div>
    <div class="progress-text">
      {{ generateCount }} / {{ generateTotal }} 完了 / 経過 {{ elapsed.toFixed(2) }} 秒 / 残り予測
      {{ remaining.toFixed(2) }} 秒 / 平均時間 {{ average.toFixed(2) }} 秒
    </div>
  </div>
</template>

<style scoped>
.progress-bar {
  margin-top: 5px;
}

.progress-text {
  font-size: 12px;
}
</style>
