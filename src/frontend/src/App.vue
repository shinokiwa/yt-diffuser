<script setup>
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
    <div id="HeaderWrapper">
        <HeaderView />
    </div>
    <div id="MainWrapper">
        <div id="MenuWrapper">
            <MenuView />
        </div>
        <div id="ContentWrapper">
            <component ref="content" v-bind:is="selectedView"></component>
        </div>
    </div>
</div>
</template>

<style scoped>
#AppWrapper {
    position: relative;
    width: 100%;
    height: 100%;
}

#HeaderWrapper {
    position: relative;
}
#MainWrapper {
    position: relative;
    top: var(--size-header-height);
    display: flex;
    flex-direction: row;
    width: 100%;
    height: calc(100% - 30px);
}

#ContentWrapper {
    padding-left: 50px;
    width: 100%;
    height: 100%;
}
</style>
