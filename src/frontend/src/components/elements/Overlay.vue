<script setup>
/**
 * オーバーレイ
 * 
 * スロット内のコンテンツを残したまま、背景を暗くする
 * 背景部分をクリックすると、スロットコンテンツおよびオーバーレイを閉じる
 */ 
const props = defineProps({
    id: {
        type: String,
        default: ''
    }
})

const isShow = defineModel('isShow', {
    type: Boolean,
    default: false
})

const emit = defineEmits(['open', 'close']);

function show () {
    isShow.value = true
    emit('open')
}

function hide () {
    isShow.value = false
    emit('close')
}

defineExpose({
    show,
    hide,
    isShow
})
</script>

<template>
<Teleport to="body">
    <div :id="id" class="modal-window" v-if="isShow">
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
    min-width: 50%;
}
</style>
