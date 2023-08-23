<script setup>
import ProgressBar from '@/components/elements/ProgressBar.vue'
</script>

<template>
<div id="InitializingView" class="content-view">
    <div class="main window">
        <p>初期化中...</p>
        <div class="progress-bar-wrapper">
            <ProgressBar :value=100 />
        </div>
    </div>
</div>
</template>

<style scoped>
p {
    margin: 40px auto 10px;
    text-align: center;
}

.progress-bar-wrapper {
    width: 50%;
    margin: auto;
}
</style>