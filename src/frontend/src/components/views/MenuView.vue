<script setup>
import { useGlobals } from '@/composables/global';
const { currentView } = useGlobals()

function changeView(view) {
    currentView.value = view
}
</script>

<template>
<nav id="MenuView">
    <ul>
        <li role="modelmanage" v-bind:class="{ 'active': currentView === 'modelmanage' }" v-on:click="changeView('modelmanage')">
            <i class="bi-gpu-card"></i>
            <span>モデル管理</span>
        </li>
        <li role="generate" v-bind:class="{ 'active': currentView === 'generate' }" v-on:click="changeView('generate')">
            <i class="bi-cpu"></i>
            <span>画像生成</span>
        </li>
        <li role="gallery" v-bind:class="{ 'active': currentView === 'gallery' }" v-on:click="changeView('gallery')">
            <i class="bi-images"></i>
            <span>ギャラリー</span>
        </li>
    </ul>
</nav>
</template>

<style scoped>
ul {
    position: fixed;
    top: 30px; left: 0; bottom: 0; right: 0;
    width: 50px;
    height: 100%;
    background-color: var(--color-bg-menu);
    color: var(--font-color-light);
    padding-top: 10px;
}

li {
    display: flex;
    align-items: center;
    padding: 5px 10px;
    margin-bottom: 5px;
    margin-left: 5px;
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