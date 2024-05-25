<script setup>
/**
 * 画像入力エリア
 */
import { ref, onMounted } from 'vue'
import ButtonMenu from '@/components/elements/ButtonMenu.vue'

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
const image = ref(null)

function cacheBuster (src) {
    isEmpty.value = false
    const url = new URL(src, window.location.href)
    url.searchParams.set('cacheBuster', new Date().getTime())
    return url.toString()
}

function update () {
    image.value.src = cacheBuster(props.src)
}

function empty () {
    isEmpty.value = true
    image.value.src = ''
}

defineExpose({
    update,
    empty
})
</script>

<template>
<div class="image-area">
    <div
        class="source-image"
    >
        <img
            v-if="src != '' && isEmpty === false"
            :src="cacheBuster(src)"
            ref="image"
            @error="isEmpty = true"
        />
        <div
            v-else
            class="no-image"
        >
            {{ emptyMessage }}
        </div>
    </div>

    <ButtonMenu class="menu">
        <slot></slot>

    </ButtonMenu>
</div>
</template>

<style scoped>
.image-area {
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
}

.image-area .menu {
    width: 100%;
}

.image-area .source-image {
    border: 1px solid var(--color-border-window);
    margin-top: 30px;
    width: 300px;
    height: 300px;
    object-fit: cover;
    text-align: center;
}

.image-area .source-image img {
    border: 1px solid var(--color-border-window);
    width: auto; height: auto;
    max-width: 100%;
    max-height: 100%;
}
</style>