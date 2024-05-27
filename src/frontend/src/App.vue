<script setup>
/**
 * アプリ内の各エリアの配置を行うコンポーネント
 *
 * メインビューの切り替えも行う。
 */
import { VIEW_IDS } from '@/utils/enum/view'
import { useAppStateUseCase } from '@/composables/app/appStateUseCase'
const { currentView } = useAppStateUseCase().getRefs()

import HiddenView from '@/components/view/HiddenView.vue'
import InitializingView from '@/components/view/InitializingView.vue'

import MenuView from '@/components/view/MenuView.vue'

import EditorView from '@/components/view/EditorView.vue'
import ModelManageView from '@/components/view/ModelManageView.vue'
import GalleryView from '@/components/view/GalleryView.vue'

const views = {
  [VIEW_IDS.MENU]: MenuView,
  [VIEW_IDS.EDITOR]: EditorView,
  [VIEW_IDS.MODEL_MANAGE]: ModelManageView,
  [VIEW_IDS.GALLERY]: GalleryView
}
</script>

<template>
  <div id="AppWrapper">
    <header>
      <h1><i class="bi-lightbulb"></i>&nbsp;ゆとりでふーざー</h1>
    </header>
    <InitializingView v-if="currentView === VIEW_IDS.INITIALIZING" />

    <div class="main-wrapper" v-if="currentView !== VIEW_IDS.INITIALIZING">
      <MenuView class="menu-view" />
      <div class="main">
        <component class="main-view" ref="content" v-bind:is="views[currentView]"></component>
      </div>
    </div>
    <HiddenView />
  </div>
</template>

<style scoped>
#AppWrapper {
  display: flex;
  flex-direction: column;
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
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

header h1 {
  font-size: 14px;
}

.main-wrapper {
  display: flex;
  flex-direction: row;
  height: calc(100% - var(--size-header-height));
}

.menu-view {
  display: flex;
  flex-direction: row;
  width: var(--size-menu-width);
  height: 100%;
}

.main {
  display: flex;
  flex-direction: column;
  width: calc(100% - var(--size-menu-width));
  height: 100%;
  padding: 10px;
}

.main-view {
  width: 100%;
  height: 100%;
}
</style>
