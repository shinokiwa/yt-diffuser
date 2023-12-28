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
    },
    'activate': {
        type: String,
        default: ''
    }
})

</script>

<template>
<div class="window" :class="{activate: activate === '1'}">
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
    display: flex; flex-direction: column;

    background-color: var(--color-bg-base);
    border: 1px solid var(--color-border-window);
    border-radius: 4px;
    overflow: hidden;
}

.window-header {
    display:flex; flex-direction: row;
    justify-content: space-between;

    margin: 0 0 5px 0;
    padding: 5px 10px;
    border-bottom: 1px solid var(--color-border-window);
    font-size: 16px;
    font-weight: bold;
}

.window.activate:has(*:focus) .window-header {
    background: var(--color-bg-activewindow);
    color: var(--font-color-activewindow)
}

.close-button {
    text-align: center;
    border: none;
    background-color: transparent;
    font-size: 18px;
    cursor: pointer;
}

.window-contents {
    flex-grow: 1;
    padding: 10px;
    height: auto;
}
</style>