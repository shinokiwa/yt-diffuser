<script setup>
/**
 * 通知エリア下部　進捗表示エリア
 */
import { watch, ref } from 'vue';
import ProgressBar from '@/components/elements/ProgressBar.vue';
import { useStatusStore } from '@/composables/store/status';
import { useProgressStore } from '@/composables/store/progress';

import { useApi } from '@/composables/api';
const { get } = useApi()

const { status } = useStatusStore()
const { progress } = useProgressStore()

const percentage = ref(0)
const total = ref(0)
const current = ref(0)
const elapsed = ref(0)
const remaining = ref(0)
watch(progress, () => {
    const data = JSON.parse(progress.value)
    percentage.value = data.percentage
    total.value = data.total
    current.value = data.progress
    elapsed.value = Math.floor(data.elapsed) + "秒"

    if (data.remaining == -1) {
        remaining.value = '不明'
    } else {
        remaining.value = Math.ceil(data.remaining || 0) + "秒"
    }
})

function stop() {
    get('/api/worker/stop')
}
</script>

<template>
<div id="ProgressView">
    <div class="status">{{ status }}</div>

    <div class="progress" v-if="true || status.indexOf('download-progress') == 0">
        <div><ProgressBar :value="percentage" /></div>

        <div class="row">
            <div>{{ current }} / {{ total }}</div>
            <div>経過時間: {{ elapsed }}</div>
        </div>
        <div class="row">
            <div>{{ percentage }}%</div>
            <div>残り: {{ remaining }}</div>
        </div>
        <div class="row">
            <div></div>
            <div><button @click="stop">中断</button></div>
        </div>
    </div>
</div>
</template>

<style scoped>

.progress {
    margin-top: 5px;
}

.row {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
}

button {
    width: 80px;
    height: 30px;
    border: none;
    border-radius: 5px;
    background-color: #252c7e;
    color: var(--font-color-light);
    font-size: 14px;
    font-weight: bold;
}

button:hover {
    background-color: #3344aa;
}
</style>