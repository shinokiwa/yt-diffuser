<script setup>
/**
 * 初期化中画面
 *
 */
import { ref, watch } from 'vue'

import ProgressBar from '@/components/element/ProgressBar.vue'

import { useServerStatusUseCase } from '@/composables/server/statusUseCase'
import { useInitializeUseCase } from '@/composables/init/initializeUseCase'

const { connected } = useServerStatusUseCase()

const statusMessage = ref('待機中...')
const progress = ref(0)

watch(connected, async (curVal, oldVal) => {
  // ヘルスチェック結果がfalseからtrueに変わった際に初期化を実行
  if ((oldVal === false || typeof oldVal === 'undefined') && curVal === true) {
    statusMessage.value = '初期化中...'
    progress.value = 50

    const { init } = useInitializeUseCase()
    await init()
    progress.value = 100
  } else {
    statusMessage.value = 'サーバーの起動を待っています...'
    progress.value = 0
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
