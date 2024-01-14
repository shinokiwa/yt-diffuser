<script setup>
import { useViewStore } from '@/composables/store/view';
const { views, currentView, changeView } = useViewStore()

import { useNotificationAreaStore } from '@/composables/store/notificationArea';
const { toggle } = useNotificationAreaStore()


</script>

<template>
<nav id="MenuView">
    <ul class="top-menu">
        <li id="MenuItemModelManage" v-bind:class="{ 'active': currentView === views.MODEL_MANAGE }" v-on:click="changeView(views.MODEL_MANAGE)">
            <i class="bi-gpu-card"></i>
            <span>モデル管理</span>
        </li>
        <li id="MenuItemPromptSetting" v-bind:class="{ 'active': currentView === views.PROMPT_SETTING }" v-on:click="changeView(views.PROMPT_SETTING)">
            <i class="bi-cpu"></i>
            <span>プロンプト設定</span>
        </li>
        <li id="MenuItemGenerateBatch" v-bind:class="{ 'active': currentView === views.GENERATE_BATCH }" v-on:click="changeView(views.GENERATE_BATCH)">
            <i class="bi-cpu"></i>
            <span>連続生成</span>
        </li>
        <li id="MenuItemGallery" v-bind:class="{ 'active': currentView === views.GALLERY }" v-on:click="changeView(views.GALLERY)">
            <i class="bi-images"></i>
            <span>ギャラリー</span>
        </li>
        <li id="MenuItemEditor" v-bind:class="{ 'active': currentView === views.EDITOR }" v-on:click="changeView(views.EDITOR)">
            <i class="bi-pencil-square"></i>
            <span>画像編集</span>
        </li>
    </ul>
    <ul class="bottom-menu">
        <li id="MenuItemNotification" v-on:click="toggle()">
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