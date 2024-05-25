<script setup>
/**
 * アプリ内の各エリアの配置を行うコンポーネント
 * 
 * メインビューの切り替えも行う。
 */
import { shallowRef, watch, onMounted } from 'vue'

import InitializingView from '@/components/views/InitializingView.vue'

import MenuView from '@/components/views/MenuView.vue'
import NotificationView from '@/components/views/NotificationView.vue'
import ModelManageView from '@/components/views/ModelManageView.vue'
import PromptSettingView from '@/components/views/PromptSettingView.vue'
import GeneratorView from '@/components/views/GeneratorView.vue'
import GalleryView from '@/components/views/GalleryView.vue'
import ImageView from '@/components/views/ImageView.vue'

import { useViewStore } from '@/composables/store/view';
const { views, currentView } = useViewStore()

const selectedView = shallowRef(null)
watch(currentView, ()=>{
    switch (currentView.value) {
        case (views.MODEL_MANAGE):
            selectedView.value = ModelManageView
            break
        case (views.PROMPT_SETTING):
            selectedView.value = PromptSettingView
            break
        case (views.GENERATE_BATCH):
            selectedView.value = GeneratorView
            break
        case (views.GALLERY):
            selectedView.value = GalleryView
            break
    }
})

</script>

<template>
<div id="AppWrapper">
    <header>
        <h1><i class="bi-lightbulb"></i>&nbsp;ゆとりでふーざー</h1>
    </header>

    <InitializingView v-if="currentView === views.INITIALIZING" />

    <div class="main-wrapper" v-if="currentView !== views.INITIALIZING">
        <MenuView class="menu-view" />
        <div class="main">
            <component class="main-view" ref="content" v-bind:is="selectedView"></component>
        </div>
        <NotificationView />
    </div>

    <ImageView />
</div>
</template>

<style scoped>
#AppWrapper {
    display: flex; flex-direction: column;
    margin: 0;
    width: 100%;
    height: 100%;
}

header {
    width: 100%;
    height: var(--size-header-height);
    background-color: var(--color-bg-header);
    padding: 4px 5px;
    color: var(--font-color-light);
    display: flex; flex-direction: row; justify-content: space-between;
}

header h1 {
    font-size: 14px;
}

.main-wrapper {
    display: flex; flex-direction: row;
    height: calc(100% - var(--size-header-height));
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