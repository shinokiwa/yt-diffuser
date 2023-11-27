<script setup>
import { useViewStore } from '@/composables/store/view';
import { useNotificationStore } from '@/composables/store/notification';

const { toggleNotificationArea } = useNotificationStore()

const {
    currentView,
    changeView,
    MODEL_MANAGE,
    GENERATE,
    GALLERY
} = useViewStore()

</script>

<template>
<nav id="MenuView">
    <ul class="top-menu">
        <li role="modelmanage" v-bind:class="{ 'active': currentView === MODEL_MANAGE }" v-on:click="changeView(MODEL_MANAGE)">
            <i class="bi-gpu-card"></i>
            <span>モデル管理</span>
        </li>
        <li role="generate" v-bind:class="{ 'active': currentView === GENERATE }" v-on:click="changeView(GENERATE)">
            <i class="bi-cpu"></i>
            <span>画像生成</span>
        </li>
        <li role="gallery" v-bind:class="{ 'active': currentView === GALLERY }" v-on:click="changeView(GALLERY)">
            <i class="bi-images"></i>
            <span>ギャラリー</span>
        </li>
    </ul>
    <ul class="bottom-menu">
        <li role="notification" v-on:click="toggleNotificationArea()">
            <i class="bi-chat-right"></i>
            <span>通知を表示</span>
        </li>
    </ul>
</nav>
</template>

<style scoped>
nav {
    background-color: var(--color-bg-menu);
    color: var(--font-color-light);
    padding-top: 10px;
}

ul {
    position: fixed;
    z-index: 100;
}

ul.bottom-menu {
    bottom: 20px;
}

li {
    display: flex; align-items: center;

    padding: 5px 10px;
    margin: 0 0 5px 5px;

    width: 40px;
    transition: width 0.5s ease;
    overflow: hidden;
    background-color: var(--color-bg-header);
    cursor: pointer;
    border-radius: 4px;
}

li.active {
    padding: 3px 8px;
    border:2px solid var(--color-bg-focus)
}

li:hover {
    width: 150px;
}

li i {
    font-size: 20px;
}

li span {
    display: none;
    margin-left: 10px;
    white-space: nowrap;
}

li:hover span {
    display: inline;
}

</style>