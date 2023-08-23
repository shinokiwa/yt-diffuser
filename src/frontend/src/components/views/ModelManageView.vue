<script setup>
import Overlay from '@/components/elements/Overlay.vue'

import { ref } from 'vue'
import { useGlobals } from '@/composables/global';
const { currentView } = useGlobals()

const overlay = ref(null)

function edit () {
    overlay.value.show()
}

</script>

<template>
<div id="ModelManageView" class="content-view">
    <div class="main window">
        <h2>モデル一覧</h2>
        <div id="ModelList">
            <div class="model-card new-model" @click="edit()">
                <span class="add-button">
                    <i class="bi-plus"></i>
                </span>
            </div>
        </div>
    </div>
    <Overlay ref="overlay"></Overlay>
</div>
</template>

<style scoped>
#ModelList {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: left;
}
.model-card {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 250px;
    height: 400px;
    border: 1px solid var(--color-border-window);
    border-radius: 4px;
    margin: 10px;
}

.model-card.new-model {
    cursor: pointer;
}

.model-card .add-button {
    text-align: center;
    font-size: 100px;
    color: var(--color-border-window);
}
</style>