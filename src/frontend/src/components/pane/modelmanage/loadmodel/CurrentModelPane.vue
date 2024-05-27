<script setup>
/**
 * モデル管理ビュー モデル選択エリア 読み込み済みモデル表示エリア
 */
//import { useGenerateStatus } from '@/composables/api/generate/status'
//const { status, baseModelLabel, loraModelLabel, controlnetModelLabel } = useGenerateStatus()
</script>

<template>
  <div id="CurrentModelPane">
    <h3>現在のモデル</h3>
    <div v-if="status === 'exit' || status === 'empty' || status === ''" class="current-model">
      なし
    </div>
    <div v-else>
      <div>
        <span v-if="status === 'loading'">読み込み中</span>
        <span v-if="status === 'ready'">読み込み完了</span>
        <span v-if="status === 'compiling'">コンパイル中</span>
        <span v-if="status === 'generating'">生成中</span>
        <span v-if="status === 'error'">エラー</span>
      </div>
      <div class="name">{{ baseModelLabel }}</div>
      <div class="info">
        <div v-if="loraModelLabel !== ''">LoRA : {{ loraModelLabel }}</div>
        <div v-if="controlnetModelLabel !== ''">controlNet : {{ controlnetModelLabel }}</div>
      </div>
    </div>
  </div>
</template>
