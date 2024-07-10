<script setup>
/**
 * 初期化中画面
 *
 */
import { ref, watch } from 'vue'

import ProgressBar from '@/components/element/ProgressBar.vue'

import { useInitializeUseCase, useAppStateUseCase } from '@/composables'

const { isConnected } = useAppStateUseCase().getRefs()

const statusMessage = ref('待機中...')
const progress = ref(0)

watch(isConnected, async (value) => {
  if (value) {
    // ヘルスチェック結果がfalseからtrueに変わった際に初期化を実行
    statusMessage.value = '初期化中...'
    progress.value = 50

    const { init } = useInitializeUseCase()
    await init()
    progress.value = 100
  }
})
</script>

<template>
  <div id="InitializingView">
    <p>{{ statusMessage }}</p>
    <div class="progress-bar-wrapper">
      <ProgressBar :value="progress" height="20" />
    </div>
  </div>
</template>

<style scoped>
#InitializingView {
  width: 100%;
  height: 100%;
}

#InitializingView p {
  margin: 100px auto 10px;
  text-align: center;
}

#InitializingView .progress-bar-wrapper {
  width: 50%;
  margin: auto;
}
</style>
