<script setup>
/**
 * エディタービュー 生成結果表示エリア 進捗表示
 */
import ProgressBar from '@/components/element/ProgressBar.vue'
import { useGenerateStatusEventUseCase } from '@/composables/generate/statusUseCase'
const useCase = useGenerateStatusEventUseCase()

const {
  generateTotal,
  generateCount,

  percentage,
  elapsed,
  remaining,
  average
} = useCase.getRefs()
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
