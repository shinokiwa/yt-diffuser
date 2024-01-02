<script setup>
/**
 * アプリ内の各エリアの配置を行うコンポーネント
 * 
 * メインビューの切り替えも行う。
 */
import { shallowRef, watchEffect, onMounted } from 'vue'

import HeaderView from '@/components/views/HeaderView.vue'
import ProgressBar from '@/components/elements/ProgressBar.vue'

import MenuView from '@/components/views/MenuView.vue'
import NotificationView from '@/components/views/NotificationView.vue'
import ModelManageView from '@/components/views/ModelManageView.vue'
import PromptSettingView from '@/components/views/PromptSettingView.vue'
import GeneratorView from '@/components/views/GeneratorView.vue'
import GalleryView from '@/components/views/GalleryView.vue'

import { useAppStore } from '@/composables/store/app';
import { useViewStore } from '@/composables/store/view';
import { useModel } from '@/composables/api/res/model'

const { readyState, ready } = useAppStore()
const {
    changeView,
    currentView,
    MODEL_MANAGE,
    PROMPT_SETTING,
    GENERATE_BATCH,
    GALLERY,
    EDITOR
} = useViewStore()
const { getModels, allModels } = useModel()

/**
 * 初期化処理
 * 
 * 前回使用モデルを取得
 * 取得できた場合は生成ビュー表示
 * モデル一覧を取得
 * モデルがある場合はモデルセットアップ表示
 * モデルがない場合はモデル管理表示
 */
onMounted(async ()=>{
    await getModels()

    if (allModels.value.length == 0) {
        changeView(MODEL_MANAGE)
    }

    ready()
})

const selectedView = shallowRef(null)
watchEffect(()=>{
    switch (currentView.value) {
        case (MODEL_MANAGE):
            selectedView.value = ModelManageView
            break
        case (PROMPT_SETTING):
            selectedView.value = PromptSettingView
            break
        case (GENERATE_BATCH):
            selectedView.value = GeneratorView
            break
        case (GALLERY):
            selectedView.value = GalleryView
            break
    }
})

</script>

<template>
<div id="AppWrapper">
    <HeaderView class="header-view"></HeaderView>

    <div id="InitializingView" class="main-wrapper" v-if="readyState == false">
        <div class="main">
            <div class="main-view">
                <p>初期化中...</p>
                <div class="progress-bar-wrapper">
                    <ProgressBar :value=100 />
                </div>
            </div>
       </div>
    </div>

    <div class="main-wrapper" v-if="readyState == true">
        <MenuView class="menu-view"></MenuView>
        <div class="main">
            <component class="main-view" ref="content" v-bind:is="selectedView"></component>
        </div>
    </div>
    <NotificationView></NotificationView>
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

#InitializingView p {
    margin: 40px auto 10px;
    text-align: center;
}

#InitializingView .progress-bar-wrapper {
    width: 50%;
    margin: auto;
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