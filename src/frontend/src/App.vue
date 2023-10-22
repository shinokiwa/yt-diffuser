<script setup>
/**
 * アプリ内の各エリアの配置を行うコンポーネント
 * 
 * メインビューの切り替えも行う。
 */
import { shallowRef, watchEffect } from 'vue'
import HeaderView from '@/components/views/HeaderView.vue'
import MenuView from '@/components/views/MenuView.vue'

import InitializingView from '@/components/views/InitializingView.vue'
import ModelManageView from '@/components/views/ModelManageView.vue'

import { useGlobals } from '@/composables/global';
const { init, currentView } = useGlobals()

init()

const selectedView = shallowRef(InitializingView)
watchEffect(()=>{
    switch (currentView.value) {
        case ('initialize'):
            selectedView.value = InitializingView
            break
        case ('modelmanage'):
            selectedView.value = ModelManageView
            break
    }
})

</script>

<template>
<div id="AppWrapper">
    <HeaderView class="header-view"></HeaderView>
    <div class="main-wrapper">
        <MenuView class="menu-view"></MenuView>
        <div class="main">
            <component class="main-view" ref="content" v-bind:is="selectedView"></component>
        </div>
    </div>
</div>
</template>

<style scoped>
#AppWrapper {
    display: flex; flex-direction: column;
    margin: 0;
    width: 100%;
    height: 100%;
}

.header-view {
    width: 100%;
    height: var(--size-header-height);
}

.main-wrapper {
    display: flex; flex-direction: row;
    height: 100%;
}

.menu-view {
    display: flex; flex-direction: row;
    width: var(--size-menu-width);
    height: 100%;
}

.main {
    display: flex; flex-direction: column;
    width: calc(100% - var(--size-menu-width));
    height: 100%;
    padding: 10px;
}

.main-view {
    width: 100%;
    height: 100%;
}
</style>