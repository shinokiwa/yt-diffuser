<script setup>
/**
 * ヘルスチェック用の非表示エリア
 *
 * - 初回表示時にヘルスチェックを行う。
 * - 成功後は30秒ごとにヘルスチェックを行い、失敗した場合は画面をリロードする。
 * - 失敗時は5秒ごとに再度ヘルスチェックを行う。
 */
import { onMounted, onUnmounted, watch } from 'vue'

import { useServerStatusUseCase } from '@/composables/server/statusUseCase'
const { disconnected, open, close } = useServerStatusUseCase()

watch(disconnected, () => {
  if (disconnected.value) {
    window.alert('サーバーから切断されました。画面をリロードします。')
    window.location.reload()
  }
})

onMounted(() => {
  open()
})

onUnmounted(() => {
  close()
})
</script>

<template>
  <div style="display: none"></div>
</template>
