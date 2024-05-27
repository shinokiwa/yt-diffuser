<script setup>
/**
 * 左サイドバーのメニュー
 *
 */
import { VIEW_IDS } from '@/utils/enum/view'
import { useAppStateUseCase } from '@/composables/app/appStateUseCase'
const appState = useAppStateUseCase()
const { currentView } = appState.getRefs()
</script>

<template>
  <nav id="MenuFrame">
    <ul class="top-menu">
      <li
        id="MenuItemModelManage"
        v-bind:class="{ active: currentView === VIEW_IDS.MODEL_MANAGE }"
        v-on:click="appState.changeView(VIEW_IDS.MODEL_MANAGE)"
      >
        <i class="bi-gpu-card"></i>
        <span>モデル管理</span>
      </li>

      <li
        id="MenuItemGallery"
        v-bind:class="{ active: currentView === VIEW_IDS.GALLERY }"
        v-on:click="appState.changeView(VIEW_IDS.GALLERY)"
      >
        <i class="bi-images"></i>
        <span>画像一覧</span>
      </li>

      <li
        id="MenuItemEditor"
        v-bind:class="{ active: currentView === VIEW_IDS.EDITOR }"
        v-on:click="appState.changeView(VIEW_IDS.EDITOR)"
      >
        <i class="bi-pencil-square"></i>
        <span>画像編集</span>
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

li {
  display: flex;
  align-items: center;

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
  border: 2px solid var(--color-bg-focus);
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
