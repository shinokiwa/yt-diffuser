<script setup>
// オーバーレイ
import { ref } from 'vue';

const isShow = ref(false)

const show = ()=> isShow.value = true
const hide = ()=> isShow.value = false

defineExpose({
    show,
    hide,
    isShow
})
</script>

<template>
<Teleport to="body">
    <div class="modal-window" v-if="isShow">
        <div class="overlay" @click="hide"></div>
        <div class="modal-view">
            <slot />
        </div>
    </div>
</Teleport>
</template>

<style scoped>
.overlay {
    position: fixed;
    z-index: 100;
    top: 0; bottom:0; right: 0; left: 0;
    background-color:rgba(33, 33, 33, 0.8);
    transition: opacity 0.3s ease;
}

.modal-view {
    position: fixed;
    z-index: 1000;
    box-sizing: content-box;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    margin: auto;
    padding: 20px;
    background-color: var(--color-bg-window);
    border: 1px solid var(--color-border-window);
    border-radius: 5px;
}

</style>
