<script setup>
/**
 * 通知エリア下部　進捗表示エリア
 */
import { watch, ref } from 'vue';
import ProgressBar from '@/components/elements/ProgressBar.vue';
import { useGenerateProgress } from '@/composables/api/generate/progress'

const {
    generateTotal,
    generateCount,

    stepsTotal,
    stepsCount,

    percentage,
    elapsed,
    remaining,
    average,

    close
} = useGenerateProgress()

</script>

<template>
<div id="ProgressView">
    <div class="progress" v-if="generateTotal > 0">
        <div>{{ generateCount }} / {{ generateTotal }} 完了(平均時間 {{ average.toFixed(2) }}秒)</div>
        <div><ProgressBar :value="percentage" /></div>

        <div class="row">
            <div>経過時間: {{ elapsed.toFixed(2) }}</div>
        </div>
        <div class="row">
            <div>{{ percentage.toFixed(2) }}%</div>
            <div>残り: {{ remaining.toFixed(2) }}</div>
        </div>
        <div class="row">
            <div></div>
            <div><button>中断</button></div>
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