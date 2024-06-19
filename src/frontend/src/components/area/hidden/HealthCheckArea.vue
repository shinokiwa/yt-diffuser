<script setup>
/**
 * ヘルスチェック用の非表示エリア
 */
//import { onMounted, onUnmounted, watch } from 'vue'

import { useGenerateStatusEventUseCase } from '@/composables/generate/statusUseCase'
useGenerateStatusEventUseCase()
</script>

<template>
  <div style="display: none"></div>
</template>
