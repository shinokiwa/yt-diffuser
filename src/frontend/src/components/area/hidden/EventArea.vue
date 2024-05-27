<script setup>
/**
 * イベント動作用の非表示エリア
 *
 * - サーバーイベント受信用のSSEを開始する。
 * - 必要に応じてトーストを表示する。
 */
import { useServerEventUseCase } from '@/composables/server/eventUseCase'
const { serverEvent } = useServerEventUseCase()
</script>

<template>
  <div style="display: none"></div>
</template>
