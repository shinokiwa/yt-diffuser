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

import { useViewStore } from '@/composables/store/view';
import { useModel } from '@/composables/api/res/model'
import { useLatestForm } from '@/composables/api/res/form/latest'
import { useForm } from '@/composables/store/form'
import { useGenerateStatus } from '@/composables/api/generate/status'

const { view } = useViewStore()

onMounted(healthCheck)

/**
 * サーバーが起動するのを待つ
 */
async function healthCheck () {
    try {
        const response = await fetch('/api/health')
        if (response.ok) {
            await init()
        } else {
            setTimeout(healthCheck, 3000)
        }
    } catch (e) {
        setTimeout(healthCheck, 3000)
    }
}

/**
 * 初期化処理
 * 
 * 前回使用モデルを取得
 * 取得できた場合は生成ビュー表示
 * モデル一覧を取得
 * モデルがある場合はモデルセットアップ表示
 * モデルがない場合はモデル管理表示
 */
async function init () {
    useGenerateStatus()

    const { getModels, allModels } = useModel()
    await getModels()

    const { getLatestForm } = useLatestForm()
    await getLatestForm()

    if (allModels.value.length == 0) {
        view.change(view.views.MODEL_MANAGE)
    } else {
        view.change(view.views.MODEL_MANAGE)
    }
}

const viewNumber = view.getCurrent()
const selectedView = shallowRef(null)
watchEffect(()=>{
    switch (viewNumber.value) {
        case (view.views.MODEL_MANAGE):
            selectedView.value = ModelManageView
            break
        case (view.views.PROMPT_SETTING):
            selectedView.value = PromptSettingView
            break
        case (view.views.GENERATE_BATCH):
            selectedView.value = GeneratorView
            break
        case (view.views.GALLERY):
            selectedView.value = GalleryView
            break
    }
})

</script>

<template>
<div id="AppWrapper">
    <HeaderView class="header-view"></HeaderView>

    <div id="InitializingView" class="main-wrapper" v-if="viewNumber === view.views.INITIALIZING">
        <div class="main">
            <div class="main-view">
                <p>初期化中...</p>
                <div class="progress-bar-wrapper">
                    <ProgressBar :value=100 />
                </div>
            </div>
       </div>
    </div>

    <div class="main-wrapper" v-if="viewNumber !== view.views.INITIALIZING">
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