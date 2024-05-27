<script setup>
/**
 * 非表示フレーム
 *
 * 通常時は非表示のセクションと、常駐するコンポーザブルを管理する
 */
import HealthCheckArea from '@/components/area/hidden/HealthCheckArea.vue'
import EventArea from '@/components/area/hidden/EventArea.vue'
</script>

<template>
  <div>
    <HealthCheckArea />
    <EventArea />
  </div>
</template>
