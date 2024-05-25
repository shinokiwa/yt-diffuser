<script setup>
/**
 * 生成の詳細設定エリア
 */
import FormElement from '@/components/elements/FormElement.vue'

const width = defineModel('width', {type: Number, default: 1024})
const height = defineModel('height', {type: Number, default: 1024})
const scheduler = defineModel('scheduler', {type: String, default: 'ddim'})
const inferenceSteps = defineModel('inferenceSteps', {type: Number, default: 50})
const guidanceScale = defineModel('guidanceScale', {type: Number, default: 8.0})

</script>

<template>
<FormElement label="詳細設定">
    <div class="prompt-grid">
        <label for="Width">幅(px)</label>
        <input type="number" id="Width" v-model="width" />

        <label for="Height">高さ(px)</label>
        <input type="number" id="Height" v-model="height" />

        <label for="Scheduler">スケジューラー</label>
        <select id="Scheduler" label="スケジューラー" v-model="scheduler">
            <option value="ddim">DDIM</option>
            <option value="pndm">PNDM</option>
            <option value="deis">DEIS Multi</option>
            <option value="dpms-singlestep">DPM-Solver++ (Singlestep)</option>
            <option value="dpms-multistep">DPM-Solver++ (Multistep)</option>
            <option value="euler">Euler Discrete</option>
            <option value="euler-ancestral">Euler Ancestral</option>
            <option value="lcm">LCM</option>
        </select>

        <label for="Steps">ステップ数</label>
        <input type="number" id="Steps" v-model="inferenceSteps" />
    
        <label for="GuidanceScale">ガイダンススケール</label>
        <input type="number" id="GuidanceScale" v-model="guidanceScale" />
    </div>
</FormElement>
</template>

<style scoped>
.prompt-grid {
    display: grid;
    grid-template-columns: 180px 1fr;
}

.prompt-grid > * {
    margin: 0.5em 0;
}

.prompt-grid > label {
    display: block;
}

.prompt-grid > input, .prompt-grid > select {
    display: block;
    border: 1px solid var(--color-border-window);
    padding: 2px 5px;
}

</style>