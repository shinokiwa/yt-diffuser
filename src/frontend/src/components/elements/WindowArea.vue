<script setup>
/**
 * ウィンドウ形状のベースとなるコンポーネント
 * 
 * @prop {String} window-title ウィンドウのタイトル
 * @prop {function} close-button 閉じるボタンを押したときの処理
 */
defineProps({
    'windowTitle': {
        type: String,
        default: ''
    },
    'closeButton': {
        type: Function,
        default: null
    }
})

</script>

<template>
<div class="window">
    <header class="window-header" v-if="windowTitle">
        <div>{{ windowTitle }}</div>
        <button class="close-button" v-if="closeButton" @click="closeButton"><i class="bi-x"></i></button>
    </header>
    <div class="window-contents">
        <slot />
    </div>
</div>
</template>

<style scoped>
.window {
    background-color: var(--color-bg-base);
    border: 1px solid var(--color-border-window);
    border-radius: 4px;
}

.window-header {
    display:flex; flex-direction: row;
    justify-content: space-between;

    margin: 5px 0;
    padding: 0 10px;
    border-bottom: 1px solid var(--color-border-window);
    font-size: 16px;
    font-weight: bold;
}

.close-button {
    text-align: center;
    border: none;
    background-color: transparent;
    font-size: 18px;
    cursor: pointer;
}

.window-contents {
    padding: 10px;
    height: auto;
}
</style>