<script setup>
import { ref, defineProps, watchEffect } from 'vue';

const props = defineProps ({
    value: Number,
    height: {
        type: [Number, String],
        default: 20
    }
})

const progress = ref(0)
watchEffect(()=> {
    progress.value = props.value
})

</script>

<template>
<div class="progress-bar" :style="'height:' + height + 'px;'">
    <div 
        class="bar"
        :style='{
            width: progress + "%"
        }'
    ></div>
</div>
</template>

<style scoped>
.progress-bar {
    position: relative;
    width: 100%;
    background-color: #cccccc;
    border: 1px solid #999999;
    border-radius: 5px;
    overflow: hidden;
    box-sizing: border-box;
}

.bar {
    background-color: blue;
    height: 100%;

    -webkit-transition: width .2s ease-in-out;
    transition: width .2s ease-in-out;

    -webkit-animation: 1s linear infinite progress-bar-stripes;
    animation: 1s linear infinite progress-bar-stripes;
    background-image: linear-gradient(45deg,rgba(255,255,255,.15) 25%,transparent 25%,transparent 50%,rgba(255,255,255,.15) 50%,rgba(255,255,255,.15) 75%,transparent 75%,transparent);
    background-size: 1rem 1rem;
}

@keyframes progress-bar-stripes {
    0% { background-position-x: 15px; }
}

</style>