<script setup>
/**
 * 画像表示部分
 * 画像の有無を確認してから表示する。
 */
import { ref, onUpdated } from 'vue'
const props = defineProps({
    src: {
        type: String,
        default: ''
    },
    emptyMessage: {
        type: String,
        default: '画像をドラッグするか、ボタン操作で画像を選択してください。'
    }
})

const isEmpty = ref(false)
const imageSource = ref('')

function update () {
    isEmpty.value = false
}

function empty () {
    isEmpty.value = true
}

defineExpose({
    update,
    empty
})

</script>

<template>
<div class="source-image">
    <img
        v-if="isEmpty === false"
        :src="src  + '?cacheBuster=' + new Date().getTime()"
        @error="isEmpty = true"
    />
    <div
        v-else
        class="no-image"
    >
        {{ emptyMessage }}
    </div>
</div>
</template>

<style scoped>
.source-image {
    border: 1px solid var(--color-border-window);
    margin-top: 30px;
    width: 300px;
    height: 300px;
    object-fit: cover;
    text-align: center;
}

.source-image img {
    border: 1px solid var(--color-border-window);
    width: auto; height: auto;
    max-width: 100%;
    max-height: 100%;
}
</style>