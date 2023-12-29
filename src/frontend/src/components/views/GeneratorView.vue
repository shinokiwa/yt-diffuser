<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import WindowArea from '@/components/elements/WindowArea.vue'
import TempGalleryWindow from '@/components/views/windows/TempGalleryWindow.vue'

import Overlay from '@/components/elements/Overlay.vue'
import FormGrid from '@/components/elements/FormGrid.vue'
import InputText from '@/components/elements/InputText.vue'

import { useGenerateImage } from '@/composables/api/generate/image'
const { start_generate } = useGenerateImage()

function submit () {
    start_generate(prompt.value)
}

const prompt = ref(null)

</script>

<template>
<WindowArea id="GeneratorView" window-title="画像生成">
    <div id="GeneratorArea">
        <WindowArea id="InputArea" window-title="入力情報">
            <div class="body">
                <div class="input">
                    <textarea placeholder="入力テキストを入力して下さい。" v-model="prompt"></textarea>
                </div>
                <div class="button">
                    <button @click="submit()">生成</button>
                </div>
            </div>
        </WindowArea>
        <TempGalleryWindow id="OutputArea" />
    </div>
</WindowArea>
</template>

<style scoped>
#GeneratorArea{
    display: flex;
    flex-direction: row;
    height: 100%;
}

#InputArea {
    width: 500px;
    margin-right: 10px;
}

/** ここは暫定 **/
#InputArea textarea {
    width: 100%;
    height: 15em;
}

#OutputArea {
    flex-grow: 1;
    width: min-content;
}

</style>