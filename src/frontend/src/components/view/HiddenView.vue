<script setup>
/**
 * 非表示フレーム
 *
 * 通常時は非表示のセクションと、常駐するコンポーザブルを管理する
 */
import HealthCheckArea from '@/components/area/hidden/HealthCheckArea.vue'
import ToastArea from '@/components/area/hidden/ToastArea.vue'
</script>

<template>
  <div>
    <ToastArea />
    <HealthCheckArea />
  </div>
</template>
